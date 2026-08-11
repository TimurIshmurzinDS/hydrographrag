import json
import os
import time
import ast
import logging
import re
import subprocess
import tempfile
import shutil
import math
from tqdm import tqdm

# Импорты ядра GeoGraphRAG
from core.database import HydroDatabase
from core.embeddings import EmbeddingsManager
from agents.identifier import DemandIdentifier
from agents.retriever import GraphRetriever
from planner.generator import SolutionPlanner

# Настройки логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

def restart_ollama():
    """Перезапуск Ollama для очистки VRAM (адаптировано для Windows)"""
    logging.info("🔄 Очистка VRAM: Перезапуск Ollama...")
    try:
        subprocess.run(["taskkill", "/F", "/IM", "ollama.exe", "/T"], capture_output=True, check=False)
        time.sleep(5) 
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NEW_CONSOLE)
        logging.info("⏳ Ожидание инициализации сервера (15 сек)...")
        time.sleep(15)
        logging.info("✅ Ollama успешно перезапущена.")
    except Exception as e:
        logging.error(f"⚠️ Ошибка при перезапуске Ollama: {e}")

# Пути к файлам
EVAL_DIR = os.path.dirname(os.path.abspath(__file__))
GROUND_TRUTH_PATH = os.path.join(EVAL_DIR, "ground_truth.json")
GENERATION_OUTPUT_PATH = os.path.join(EVAL_DIR, "generation_results.json")
RESULTS_DIR = os.path.join(EVAL_DIR, "results")

# Список моделей для тестирования
GENERATOR_MODELS = [
    "qwen2.5-coder:7b",
   "qwen2.5-coder:32b",
    "llama3.1:8b",
    "gemma2:27b",
   "codestral",
   "mistral-nemo",
    "gemma4:31b"
]

# 7 режимов Ablation Study (жестко заданные конфигурации)
# 9 режимов Ablation Study (включая новые)
ABLATION_MODES = {
    "Baseline": {"type": "baseline", "use_cda": False, "use_wkt": False, "use_ood": True, "use_template": True, "use_sandbox": True},
    "VectorRAG": {"type": "vector_rag", "use_cda": False, "use_wkt": False, "use_ood": True, "use_template": True, "use_sandbox": True},
    "HydroGraphRAG": {"type": "hydrographrag", "use_cda": True, "use_wkt": True, "use_ood": True, "use_template": True, "use_sandbox": True},
    "HydroGraphRAG_no_CDA": {"type": "hydrographrag", "use_cda": False, "use_wkt": True, "use_ood": True, "use_template": True, "use_sandbox": True},
    "HydroGraphRAG_no_WKT": {"type": "hydrographrag", "use_cda": True, "use_wkt": False, "use_ood": True, "use_template": True, "use_sandbox": True},
    "HydroGraphRAG_no_Template": {"type": "hydrographrag", "use_cda": True, "use_wkt": True, "use_ood": True, "use_template": False, "use_sandbox": True},
    "HydroGraphRAG_no_OOD": {"type": "hydrographrag", "use_cda": True, "use_wkt": True, "use_ood": False, "use_template": True, "use_sandbox": True},
    "HydroGraphRAG_no_Cache": {"type": "hydrographrag", "use_cda": True, "use_wkt": True, "use_ood": True, "use_template": True, "use_sandbox": True},
    "HydroGraphRAG_no_Sandbox": {"type": "hydrographrag", "use_cda": True, "use_wkt": True, "use_ood": True, "use_template": True, "use_sandbox": False}
}

class GenerationPipeline:
    def __init__(self):
        logging.info("⏳ Инициализация среды тестирования...")
        self.db = HydroDatabase()
        self.embedder = EmbeddingsManager()

    def extract_python_code(self, text):
        """Умный парсер кода из markdown-блоков"""
        match = re.search(r'```python\n(.*?)\n```', text, re.DOTALL)
        if match: return match.group(1).strip()
        match_generic = re.search(r'```(.*?)```', text, re.DOTALL)
        if match_generic: return match_generic.group(1).strip()
        return text.strip()

    def extract_decision(self, text):
        """Извлекает решение об отказе из текста LLM"""
        decision_match = re.search(r'decision:\s*(ANSWER|ABSTAIN)', text, re.IGNORECASE)
        decision = decision_match.group(1).upper() if decision_match else "ANSWER"
        
        reason_match = re.search(r'abstain_reason:\s*(.*)', text, re.IGNORECASE)
        reason = reason_match.group(1).strip() if reason_match else None
        
        return decision, reason

    def check_syntax(self, code_str):
        """Проверка синтаксиса Python-кода через AST"""
        try:
            ast.parse(self.extract_python_code(code_str))
            return True
        except Exception:
            return False

    def calculate_rmse(self, stdout_str, expected_values):
        """Расчет RMSE по числовым спискам в выводе консоли"""
        if not stdout_str or not expected_values: return None
        try:
            match = re.search(r'\[([\d\.,\s\-]+)\]', stdout_str)
            if not match: return None
            actual_values = ast.literal_eval(f"[{match.group(1)}]")
            if len(actual_values) != len(expected_values): return None
            sq_error = sum((float(a) - float(e)) ** 2 for a, e in zip(actual_values, expected_values))
            return round(math.sqrt(sq_error / len(actual_values)), 4)
        except Exception:
            return None

    def execute_code(self, code_str, output_html_path, sandbox_dir, timeout=15):
        """Запуск сгенерированного кода в песочнице"""
        clean_code = self.extract_python_code(code_str)
        if not clean_code or len(clean_code.strip()) < 10:
            return False, "No valid code found", None, False

        tmp_py_path = os.path.join(sandbox_dir, "script.py")
        with open(tmp_py_path, "w", encoding="utf-8") as f:
            f.write(clean_code)

        try:
            result = subprocess.run(["python", "script.py"], cwd=sandbox_dir, capture_output=True, text=True, timeout=timeout)
            html_created = False
            
            for file in os.listdir(sandbox_dir):
                if file.endswith(".html"):
                    shutil.copy(os.path.join(sandbox_dir, file), output_html_path)
                    os.remove(os.path.join(sandbox_dir, file))
                    html_created = True
                    break
                    
            if result.returncode == 0:
                return True, "Success", result.stdout.strip(), html_created
            else:
                return False, result.stderr, None, html_created
        except Exception as e:
            return False, str(e), None, False

    def calculate_retrieval_metrics(self, retrieved_triples, expected_entities):
        """Оценка метрик поиска в графе (Precision, Recall/TDR, EER)"""
        if not expected_entities: return {"tdr": 0.0, "eer": 0.0, "status": "no_ground_truth"}
        
        retrieved_entities = set()
        technical_metadata = ['region', 'class', 'value', 'unit', 'geometry', 'haswkt', 'date']
        
        for t in retrieved_triples:
            nodes = [str(t.get('from', '')), str(t.get('to', ''))]
            for node in nodes:
                node_clean = node.strip().lower()
                if not node_clean or len(node_clean) < 3 or re.search(r'\d', node_clean): continue
                if any(tech in node_clean for tech in technical_metadata): continue
                retrieved_entities.add(node_clean)
                
        truth_nodes = set([str(e).lower() for e in expected_entities])
        matched_expected = set(expected for expected in truth_nodes if any(expected in retrieved or retrieved in expected for retrieved in retrieved_entities))
        
        tdr = len(matched_expected) / len(truth_nodes) if truth_nodes else 0.0
        expansion_ratio = round((len(retrieved_entities) - len(matched_expected)) / len(matched_expected), 2) if matched_expected else 0.0
        
        return {
            "tdr": round(tdr, 4), 
            "eer": expansion_ratio, 
            "retrieved_total": len(retrieved_entities), 
            "targets_found": len(matched_expected)
        }

    def get_vector_only_context(self, query, retriever, k=5):
        """Векторный поиск (эмуляция VectorRAG)"""
        try:
            candidates = retriever._get_all_entities()
            scored = self.embedder.find_top_matches(query, candidates, top_k=k)
            return "\n".join([f"Entity: {s[0]['name']} (Type: {s[0].get('category', 'Unknown')})" for s in scored])
        except Exception as e:
            logging.error(f"VectorRAG Context Error: {e}")
            return "No vector context found."

    def run(self):
        """Главный цикл проведения Ablation Study"""
        if not os.path.exists(GROUND_TRUTH_PATH):
            logging.error(f"❌ Файл {GROUND_TRUTH_PATH} не найден.")
            return

        with open(GROUND_TRUTH_PATH, 'r', encoding='utf-8') as f: 
            dataset = json.load(f)
            
        os.makedirs(RESULTS_DIR, exist_ok=True)
        
        if os.path.exists(GENERATION_OUTPUT_PATH):
            with open(GENERATION_OUTPUT_PATH, 'r', encoding='utf-8') as f: 
                all_results = json.load(f)
        else:
            all_results = []
            
        completed_models = [res.get('model') for res in all_results]

        for model_name in GENERATOR_MODELS:
            if model_name in completed_models:
                logging.info(f"⏭️ Модель {model_name} пропущена (уже в кэше).")
                continue
                
            restart_ollama()    
            self.db.clear_solution_graphs() 
            logging.info(f"\n🚀 СТАРТ ТЕСТА: {model_name}")
            
            safe_model_name = model_name.replace(":", "_")
            model_dir = os.path.join(RESULTS_DIR, safe_model_name)
            
            for mode in ABLATION_MODES.keys(): 
                os.makedirs(os.path.join(model_dir, mode), exist_ok=True)
            
            identifier = DemandIdentifier(model_name=model_name)
            retriever = GraphRetriever(self.db, self.embedder, model_name=model_name) 
            planner = SolutionPlanner(model_name=model_name)
            model_results = []

            for item in tqdm(dataset, desc=f"Testing {model_name}"):
                query = item['query']
                expected_entities = item.get('expected_entities', [])
                expected_values = item.get('expected_values', [])
                query_id = str(item.get("id"))
                gt_category = item.get('category', 'explicit')
                
                cda_demand = identifier.analyze_query(query)
                vec_context = self.get_vector_only_context(query, retriever)
                
                query_result = {"query_id": query_id, "category": gt_category}

                for mode_name, config in ABLATION_MODES.items():
                    start = time.time()
                    
                    if config["type"] == "baseline":
                        context_data = []
                    elif config["type"] == "vector_rag":
                        context_data = vec_context
                    else:
                        demand = cda_demand if config["use_cda"] else {'category': 'explicit', 'extracted_inputs': [query]}
                        raw_triples = retriever.find_solution_subgraph(demand)
                        context_data = raw_triples if config["use_wkt"] else [t for t in raw_triples if t.get('rel') != 'hasWKT']
                        
                    res_llm = planner.generate(
                        mode=config["type"], 
                        user_query=query, 
                        query_id=query_id, 
                        context_data=context_data,
                        use_ood_rule=config["use_ood"], 
                        use_template=config["use_template"]
                    )
                    
                    lat = round(time.time() - start, 2)
                    code_llm = self.extract_python_code(res_llm)
                    syn_llm = self.check_syntax(code_llm)
                    
                    decision, abstain_reason = self.extract_decision(res_llm)
                    
                    py_path = os.path.join(model_dir, mode_name, f"{query_id}.py")
                    html_path = os.path.join(model_dir, mode_name, f"{query_id}.html")
                    with open(py_path, "w", encoding="utf-8") as f: 
                        f.write(code_llm)
                    
                    # Изолированная песочница на уровне отдельного запроса
                    exe_llm, err_llm, stdout_llm, has_html = False, "Not Executed", None, False
                    if syn_llm and config["use_sandbox"]:
                        with tempfile.TemporaryDirectory() as local_sandbox:
                            data_src = os.path.join(EVAL_DIR, "data")
                            data_dest = os.path.join(local_sandbox, "data")
                            if os.path.exists(data_src): 
                                shutil.copytree(data_src, data_dest)
                            
                            exe_llm, err_llm, stdout_llm, has_html = self.execute_code(code_llm, html_path, sandbox_dir=local_sandbox)
                    elif syn_llm and not config["use_sandbox"]:
                        exe_llm, err_llm, stdout_llm, has_html = self.execute_code(code_llm, html_path, sandbox_dir=EVAL_DIR)
                    
                    rmse_llm = self.calculate_rmse(stdout_llm, expected_values) if exe_llm else None

                    # Собираем данные строго внутрь архитектуры
                    arch_results = {
                        "decision": decision,
                        "abstain_reason": abstain_reason,
                        "latency": lat, 
                        "syntax": syn_llm, 
                        "exec": exe_llm, 
                        "rmse": rmse_llm, 
                        "has_map": has_html
                    }
                    
                    if "hydrographrag" in config["type"]:
                        arch_results["triples"] = len(context_data) if isinstance(context_data, list) else 0
                        arch_results["retrieval"] = self.calculate_retrieval_metrics(context_data, expected_entities)
                    
                    query_result[mode_name] = arch_results

                model_results.append(query_result)

            all_results.append({"model": model_name, "metrics": model_results})
            with open(GENERATION_OUTPUT_PATH, 'w', encoding='utf-8') as f:
                json.dump(all_results, f, ensure_ascii=False, indent=4)

        logging.info("🎉 Пайплайн тестирования Ablation Study полностью завершен!")
if __name__ == "__main__":
    GenerationPipeline().run()