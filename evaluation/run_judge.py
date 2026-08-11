import json
import logging
import re
import os
import ast
from tqdm import tqdm
from langchain_ollama import ChatOllama

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# Независимый судья
JUDGE_MODEL = "qwen2.5:72b-instruct" 

EVAL_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(EVAL_DIR, "generation_results.json")
FINAL_OUTPUT_PATH = os.path.join(EVAL_DIR, "final_evaluation_results.json")
RESULTS_DIR = os.path.join(EVAL_DIR, "results") 
GROUND_TRUTH_PATH = os.path.join(EVAL_DIR, "ground_truth.json") 

class EvaluationPipeline:
    def __init__(self):
        logging.info(f"⚖️ Инициализация независимого судьи {JUDGE_MODEL} (режим 0.0 temp)...")
        self.judge = ChatOllama(model=JUDGE_MODEL, temperature=0.0)

    def _robust_json_parse(self, text):
        try:
            text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
            match = re.search(r'\{.*\}', text, re.DOTALL)
            json_str = match.group(0) if match else text
            
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                try:
                    return ast.literal_eval(json_str)
                except Exception:
                    return None
        except Exception:
            return None

    def evaluate(self, query, code_response, exec_status, gt_item):
        """Оценка 4 подтипов галлюцинаций с передачей полных gold facts."""
        status_msg = "Execution: SUCCESS" if exec_status else "Execution: FAILED"
        
        # Пункт 19: Формируем полный структурированный Gold Fact для судьи
        truth_str = f"""
        - Expected Entities: {", ".join(gt_item.get("expected_entities", []))}
        - Expected WKT (Coordinates): {", ".join(gt_item.get("expected_wkt", []))}
        - Expected Numeric Values: {", ".join(map(str, gt_item.get("expected_numeric_facts", [])))}
        - Expected Topology (Relations): {", ".join(gt_item.get("expected_topology", []))}
        """
        
        prompt = f"""
        You are a senior geospatial scientist evaluating an AI geospatial framework.
        User Query: "{query}"
        
        [GROUND TRUTH FACTS]
        {truth_str}
        
        [RUNTIME STATUS]
        {status_msg}

        Analyze the generated Python Code and evaluate it on a scale of 1 to 5.
        CRITICAL: You MUST evaluate Faithfulness by checking for 4 specific Hydrological Hallucination Subtypes against the [GROUND TRUTH FACTS].
        Score each subtype from 1 (severe hallucination/completely fabricated vs Ground Truth) to 5 (perfectly faithful/matches Ground Truth).
        
        Subtypes to evaluate:
        1. "spatial_score": Did the code hallucinate WKT coordinates that do not match the expected WKT?
        2. "numerical_score": Did the code invent water levels, flow rates, or numbers not in the expected numeric values?
        3. "topological_score": Did the code hallucinate river connections or relations?
        4. "categorical_score": Did the code fabricate sensor statuses or region names?

        Output strictly JSON:
        {{
            "semantic_score": <1-5>,
            "structural_score": <1-5>,
            "faithfulness_valid": <1-5>,
            "hallucination_subtypes": {{
                "spatial_score": <1-5>,
                "numerical_score": <1-5>,
                "topological_score": <1-5>,
                "categorical_score": <1-5>
            }},
            "reasoning": "<short explanation of faults if any>"
        }}
        """
        
        try:
            res = self.judge.invoke(prompt)
            parsed = self._robust_json_parse(res.content)
            
            if parsed and "hallucination_subtypes" in parsed:
                subtypes = parsed.pop("hallucination_subtypes")
                parsed.update(subtypes)
                return parsed
            else:
                return {
                    "semantic_score": 0, "structural_score": 0, "faithfulness_valid": 0,
                    "spatial_score": 0, "numerical_score": 0, "topological_score": 0, "categorical_score": 0,
                    "reasoning": "Judge failed to output valid JSON format."
                }
        except Exception as e:
            logging.error(f"Ошибка судьи: {e}")
            return {
                "semantic_score": 0, "structural_score": 0, "faithfulness_valid": 0,
                "spatial_score": 0, "numerical_score": 0, "topological_score": 0, "categorical_score": 0,
                "reasoning": f"Judge error: {str(e)}"
            }

    def run(self):
        if not os.path.exists(INPUT_PATH):
            logging.error(f"❌ Файл {INPUT_PATH} не найден. Сначала запусти run_generation.py")
            return
        if not os.path.exists(GROUND_TRUTH_PATH):
            logging.error(f"❌ Файл {GROUND_TRUTH_PATH} не найден.")
            return

        with open(INPUT_PATH, 'r', encoding='utf-8') as f:
            generation_data = json.load(f)

        with open(GROUND_TRUTH_PATH, 'r', encoding='utf-8') as f:
            ground_truth = json.load(f)
            
        queries_map = {str(item.get("id")): item for item in ground_truth}

        # Все 9 режимов Ablation Study (включая новые)
        modes = [
            "Baseline", 
            "VectorRAG", 
            "HydroGraphRAG",
            "HydroGraphRAG_no_CDA",
            "HydroGraphRAG_no_WKT",
            "HydroGraphRAG_no_Template",
            "HydroGraphRAG_no_OOD",
            "HydroGraphRAG_no_Cache",
            "HydroGraphRAG_no_Sandbox"
        ]

        for model_data in generation_data:
            model_name = model_data['model']
            logging.info(f"🧐 Оценка модели: {model_name}")
            
            safe_model_name = model_name.replace(":", "_")
            
            for item in tqdm(model_data['metrics'], desc=f"Judging {model_name}"):
                query_id = str(item.get('query_id'))
                gt_item = queries_map.get(query_id, {})
                query = gt_item.get("query", "Unknown query")
                category = item.get('category', 'explicit')
                
                # Пункт 6: Пропускаем OOD. Судья оценивает только валидные запросы.
                if category == "anomalous" or category == "OOD":
                    continue
                
                for m in modes:
                    if m not in item: continue
                    
                    py_path = os.path.join(RESULTS_DIR, safe_model_name, m, f"{query_id}.py")
                    
                    code_response = ""
                    if os.path.exists(py_path):
                        with open(py_path, 'r', encoding='utf-8') as f:
                            code_response = f.read()
                    else:
                        code_response = "# Файл с кодом не сгенерирован."
                        
                    exec_status = item[m].get('exec', False)
                    
                    # Передаем полный Ground Truth item судье
                    scores = self.evaluate(query, code_response, exec_status, gt_item)
                    item[m].update(scores)

        with open(FINAL_OUTPUT_PATH, 'w', encoding='utf-8') as f:
            json.dump(generation_data, f, ensure_ascii=False, indent=4)

        logging.info(f"✅ Готово! Итоговый научный отчет сохранен: {FINAL_OUTPUT_PATH}")

if __name__ == "__main__":
    EvaluationPipeline().run()