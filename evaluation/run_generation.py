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

# Импорты твоего ядра
from core.database import HydroDatabase
from core.embeddings import EmbeddingsManager
from agents.identifier import DemandIdentifier
from agents.retriever import GraphRetriever
from planner.generator import SolutionPlanner

# Настройки логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
def restart_ollama():
    print("🔄 Перезапуск Ollama для очистки VRAM...")
    try:
            # Для Linux (systemd)
        subprocess.run(["sudo", "systemctl", "restart", "ollama"], check=True)
            # Даем 10 секунд на полную инициализацию сервиса
        time.sleep(10) 
        print("✅ Ollama успешно перезапущена.")
    except Exception as e:
        print(f"⚠️ Ошибка при перезапуске Ollama: {e}")
    
# Пути к файлам
EVAL_DIR = os.path.dirname(os.path.abspath(__file__))
GROUND_TRUTH_PATH = os.path.join(EVAL_DIR, "ground_truth.json")
GENERATION_OUTPUT_PATH = os.path.join(EVAL_DIR, "generation_results.json")
RESULTS_DIR = os.path.join(EVAL_DIR, "results")

# Список моделей для теста
# Список моделей для масштабного теста
GENERATOR_MODELS = [
    "qwen2.5-coder:7b",
    "qwen2.5-coder:32b",
    "llama3.1:8b",
    "gemma2:27b",
    "codestral",
    "mistral-nemo",
   #gemma4:26b",
    "gemma4:31b",
    "llama3.3"

]

class GenerationPipeline:
    def __init__(self):
        logging.info("⏳ Инициализация среды тестирования...")
        self.db = HydroDatabase()
        self.embedder = EmbeddingsManager()

    def extract_python_code(self, text):
        """Умный и БЕЗОПАСНЫЙ парсер кода из markdown-блоков"""
        match = re.search(r'```python\n(.*?)\n```', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        
        match_generic = re.search(r'```(.*?)```', text, re.DOTALL)
        if match_generic:
            return match_generic.group(1).strip()
            
        return text.strip()

    def check_syntax(self, code_str):
        """Проверка синтаксиса Python-кода через AST"""
        try:
            ast.parse(self.extract_python_code(code_str))
            return True
        except Exception:
            return False

    def calculate_rmse(self, stdout_str, expected_values):
        """Расчет RMSE по числовым спискам в выводе консоли"""
        if not stdout_str or not expected_values:
            return None
        
        try:
            match = re.search(r'\[([\d\.,\s\-]+)\]', stdout_str)
            if not match:
                return None
                
            actual_values = ast.literal_eval(f"[{match.group(1)}]")
            
            if len(actual_values) != len(expected_values):
                return None
                
            sq_error = sum((float(a) - float(e)) ** 2 for a, e in zip(actual_values, expected_values))
            return round(math.sqrt(sq_error / len(actual_values)), 4)
        except Exception:
            return None

    def execute_code(self, code_str, output_html_path, sandbox_dir, timeout=15):
        """Запуск кода в уже существующей и подготовленной песочнице"""
        clean_code = self.extract_python_code(code_str)
        if not clean_code or len(clean_code.strip()) < 10:
            return False, "No valid code found", None, False

        # sandbox_dir — это папка, которую мы создадим один раз в методе run()
        tmp_py_path = os.path.join(sandbox_dir, "script.py")
        
        with open(tmp_py_path, "w", encoding="utf-8") as f:
            f.write(clean_code)

        try:
            result = subprocess.run(
                ["python", "script.py"], 
                cwd=sandbox_dir, # Запускаем в общей папке, где уже лежат данные
                capture_output=True, 
                text=True, 
                timeout=timeout
            )
            
            html_created = False
            for file in os.listdir(sandbox_dir):
                if file.endswith(".html"):
                    shutil.copy(os.path.join(sandbox_dir, file), output_html_path)
                    # Удаляем временный html, чтобы он не мешал следующему тесту
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
        if not expected_entities:
            return {"tdr": 0.0, "eer": 0.0, "status": "no_ground_truth"}

        # Фильтрация только значимых сущностей (исключаем технические метаданные)
        retrieved_entities = set()
        technical_metadata = ['region', 'class', 'value', 'unit', 'geometry', 'haswkt', 'date']

        for t in retrieved_triples:
            # Проверяем и субъект, и объект триплета
            nodes = [str(t.get('from', '')), str(t.get('to', ''))]
            for node in nodes:
                node_clean = node.strip().lower()
                if not node_clean or len(node_clean) < 3 or re.search(r'\d', node_clean): continue
                if any(tech in node_clean for tech in technical_metadata): continue
                retrieved_entities.add(node_clean)

        truth_nodes = set([str(e).lower() for e in expected_entities])
        matched_expected = set()
        
        # Считаем найденные целевые сущности (TDR)
        for expected in truth_nodes:
            if any(expected in retrieved or retrieved in expected for retrieved in retrieved_entities):
                matched_expected.add(expected)
        
        tdr = len(matched_expected) / len(truth_nodes)

        # Рассчитываем коэффициент расширения (EER)
        # Показывает, сколько доп. контекста (атрибутов) извлечено на 1 целевую сущность
        expansion_ratio = 0.0
        if len(matched_expected) > 0:
            extra_nodes = len(retrieved_entities) - len(matched_expected)
            expansion_ratio = round(extra_nodes / len(matched_expected), 2)

        return {
            "tdr": round(tdr, 4),
            "eer": expansion_ratio,
            "retrieved_total": len(retrieved_entities),
            "targets_found": len(matched_expected)
        }
    def get_vector_only_context(self, query, retriever, k=5):
        """Эмуляция Naive Vector RAG (Baseline 2)"""
        try:
            candidates = retriever._get_all_entities()
            scored = self.embedder.find_top_matches(query, candidates, top_k=k)
            context_strings = [f"Entity: {s[0]['name']} (Type: {s[0].get('category', 'Unknown')})" for s in scored]
            return "\n".join(context_strings)
        except Exception as e:
            logging.error(f"VectorRAG Context Error: {e}")
            return "No vector context found."

    def run(self):
        """Главный цикл проведения Ablation Study"""
        if not os.path.exists(GROUND_TRUTH_PATH):
            logging.error(f"❌ Файл {GROUND_TRUTH_PATH} не найден.")
            return

        # 1. Открываем песочницу
        with tempfile.TemporaryDirectory() as global_sandbox:
            # 2. Копируем данные ОДИН РАЗ
            data_src = os.path.join(EVAL_DIR, "data")
            data_dest = os.path.join(global_sandbox, "data")
            
            if os.path.exists(data_src):
                shutil.copytree(data_src, data_dest)
                logging.info(f"🚀 Данные загружены в глобальный sandbox: {data_dest}")

            # 3. ВСЯ ОСТАЛЬНАЯ ЛОГИКА ДОЛЖНА БЫТЬ ВНУТРИ ЭТОГО БЛОКА (с отступом!)
            with open(GROUND_TRUTH_PATH, 'r', encoding='utf-8') as f:
                dataset = json.load(f)
            os.makedirs(RESULTS_DIR, exist_ok=True)
            
            if os.path.exists(GENERATION_OUTPUT_PATH):
                with open(GENERATION_OUTPUT_PATH, 'r', encoding='utf-8') as f:
                    all_results = json.load(f)
                logging.info(f"✅ Найдено {len(all_results)} моделей в кэше. Продолжаем.")
            else:
                all_results = []
                
            completed_models = [res.get('model') for res in all_results]
            data_folder = os.path.join(os.path.dirname(EVAL_DIR), "data")

            for model_name in GENERATOR_MODELS:
                
                if model_name in completed_models:
                    logging.info(f"⏭️ Модель {model_name} пропущена.")
                    continue
                restart_ollama()    
                self.db.clear_solution_graphs() 
                logging.info(f"\n🚀 СТАРТ ТЕСТА: {model_name}")
                
                safe_model_name = model_name.replace(":", "_")
                model_dir = os.path.join(RESULTS_DIR, safe_model_name)
                
                for mode in ["baseline", "vector_rag", "geographrag"]:
                    os.makedirs(os.path.join(model_dir, mode), exist_ok=True)
                
                identifier = DemandIdentifier(model_name=model_name)
                retriever = GraphRetriever(self.db, self.embedder, model_name=model_name) 
                planner = SolutionPlanner(model_name=model_name)
                
                model_results = []

                for item in tqdm(dataset, desc=f"Тестируем {model_name}"):
                    query = item['query']
                    expected_entities = item.get('expected_entities', [])
                    expected_values = item.get('expected_values', [])
                    query_id = str(item.get("id"))
                    gt_category = item.get('category', 'explicit')

                    # --- 1. BASELINE ---
                    start = time.time()
                    res_base = planner.generate_io_response(query, query_id)
                    lat_base = round(time.time() - start, 2)
                    code_base = self.extract_python_code(res_base)
                    syn_base = self.check_syntax(code_base)
                    
                    py_path_base = os.path.join(model_dir, "baseline", f"{query_id}.py")
                    html_path_base = os.path.join(model_dir, "baseline", f"{query_id}.html")
                    
                    if syn_base:
                        exe_base, err_base, stdout_base, has_html_base = self.execute_code(
        code_base, html_path_base, sandbox_dir=global_sandbox
    )
                    else:
                        exe_base, err_base, stdout_base, has_html_base = False, "Syntax Error", None, False
                    
                    rmse_base = self.calculate_rmse(stdout_base, expected_values) if exe_base else None
                    with open(py_path_base, "w", encoding="utf-8") as f: f.write(code_base)

                    # --- 2. VECTOR RAG ---
                    vec_context = self.get_vector_only_context(query, retriever)
                    start = time.time()
                    res_vec = planner.generate_vector_rag_response(query, vec_context, query_id)
                    lat_vec = round(time.time() - start, 2)
                    code_vec = self.extract_python_code(res_vec)
                    syn_vec = self.check_syntax(code_vec)
                    
                    py_path_vec = os.path.join(model_dir, "vector_rag", f"{query_id}.py")
                    html_path_vec = os.path.join(model_dir, "vector_rag", f"{query_id}.html")
                    
                    if syn_vec:
                        exe_vec, err_vec, stdout_vec, has_html_vec = self.execute_code(
        code_vec, html_path_vec, sandbox_dir=global_sandbox
    )
                    else:
                        exe_vec, err_vec, stdout_vec, has_html_vec = False, "Syntax Error", None, False
                    
                    rmse_vec = self.calculate_rmse(stdout_vec, expected_values) if exe_vec else None
                    with open(py_path_vec, "w", encoding="utf-8") as f: f.write(code_vec)

                    # --- 3. GEOGRAPHRAG (НАШ МЕТОД) ---
                    start = time.time()
                    demand = identifier.analyze_query(query)
                    extracted_category = demand.get('category', 'unknown')
                    
                    py_path_rag = os.path.join(model_dir, "geographrag", f"{query_id}.py")
                    html_path_rag = os.path.join(model_dir, "geographrag", f"{query_id}.html")

                    # БЛОКИРОВКА АНОМАЛИЙ
                    if extracted_category == "anomalous" or gt_category == "anomalous":
                        lat_rag = round(time.time() - start, 2)
                        code_rag = "# ОТКАЗ: Запрос не относится к гидрологии бассейна."
                        syn_rag, exe_rag, has_html_rag = False, False, False
                        rmse_rag = None
                        triples = []
                        with open(py_path_rag, "w", encoding="utf-8") as f: f.write(code_rag)
                    else:
                        # Полноценный поиск в графе
                        triples = retriever.find_solution_subgraph(demand)
                        res_rag = planner.generate_geographrag_response(query, triples, query_id)
                        lat_rag = round(time.time() - start, 2)
                        code_rag = self.extract_python_code(res_rag)
                        syn_rag = self.check_syntax(code_rag)
                        
                        if syn_rag:
                            # Сделай так:
                            exe_rag, err_rag, stdout_rag, has_html_rag = self.execute_code(
        code_rag, html_path_rag, sandbox_dir=global_sandbox
    )
                        else:
                            exe_rag, err_rag, stdout_rag, has_html_rag = False, "Syntax Error", None, False
                        
                        rmse_rag = self.calculate_rmse(stdout_rag, expected_values) if exe_rag else None
                        with open(py_path_rag, "w", encoding="utf-8") as f: f.write(code_rag)
                    
                    retr_metrics = self.calculate_retrieval_metrics(triples, expected_entities)

                    # Сборка финальных данных
                    model_results.append({
                        "query_id": query_id,
                        "category": gt_category,
                        "Baseline": {"latency": lat_base, "syntax": syn_base, "exec": exe_base, "rmse": rmse_base, "has_map": has_html_base},
                        "VectorRAG": {"latency": lat_vec, "syntax": syn_vec, "exec": exe_vec, "rmse": rmse_vec, "has_map": has_html_vec},
                        "GeoGraphRAG": {
                            "latency": lat_rag, "syntax": syn_rag, "exec": exe_rag, "rmse": rmse_rag, "has_map": has_html_rag,
                            "retrieval": retr_metrics, "triples": len(triples)
                        }
                    })

                # Сохранение результатов после прохода всех вопросов одной моделью
                all_results.append({"model": model_name, "metrics": model_results})
                with open(GENERATION_OUTPUT_PATH, 'w', encoding='utf-8') as f:
                    json.dump(all_results, f, ensure_ascii=False, indent=4)

            logging.info("🎉 Пайплайн тестирования полностью завершен!")

if __name__ == "__main__":
    pipeline = GenerationPipeline()
    pipeline.run()