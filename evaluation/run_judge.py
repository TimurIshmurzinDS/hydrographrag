import json
import logging
import re
import os
import ast
import subprocess
import time
from tqdm import tqdm
from langchain_ollama import ChatOllama

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# Независимый судья (не пересекающийся с пулом легких генераторов)
JUDGE_MODEL = "qwen2.5:72b-instruct"  # Модель для оценки Faithfulness и Hallucination Subtypes

# Жесткая привязка путей к директории скрипта
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
        """Очистка вывода от <think> и markdown + защита от кривого JSON."""
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

    def evaluate(self, query, code_response, exec_status, mode, expected_entities):
        """Оценка с использованием эталонных сущностей и 4 подтипов галлюцинаций."""
        status_msg = "Execution: SUCCESS" if exec_status else "Execution: FAILED"
        truth_str = ", ".join(expected_entities) if expected_entities else "None specified"
        
        prompt = f"""
        You are a senior geospatial scientist evaluating an AI geospatial framework.
        User Query: "{query}"
        Expected Targets: {truth_str}
        Runtime Status: {status_msg}

        Analyze the Python Code and evaluate it on a scale of 1 to 5.
        CRITICAL: You MUST evaluate Faithfulness by checking for 4 specific Hydrological Hallucination Subtypes.
        Score each subtype from 1 (severe hallucination/completely fabricated) to 5 (perfectly faithful/no hallucination).
        
        Subtypes to evaluate:
        1. "spatial_score": Are WKT coordinates or spatial locations fabricated?
        2. "numerical_score": Are water levels, flow rates, or other numerical metrics invented?
        3. "topological_score": Are river connections (tributaries, upstream/downstream) hallucinated?
        4. "categorical_score": Are sensor statuses, water classes, or region names made up?

        Output strictly JSON:
        {{
            "semantic_score": <1-5>,
            "structural_score": <1-5>,
            "faithfulness_score": <1-5>,
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
                    "semantic_score": 0, "structural_score": 0, "faithfulness_score": 0,
                    "spatial_score": 0, "numerical_score": 0, "topological_score": 0, "categorical_score": 0,
                    "reasoning": "Judge failed to output valid JSON format."
                }
        except Exception as e:
            logging.error(f"Ошибка судьи: {e}")
            return {
                "semantic_score": 0, "structural_score": 0, "faithfulness_score": 0,
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
            
        queries_map = {str(item.get("id")): item.get("query") for item in ground_truth}

        # Все 7 режимов Ablation Study
        modes = [
            "Baseline", 
            "VectorRAG", 
            "GeoGraphRAG",
            "GeoGraphRAG_no_CDA",
            "GeoGraphRAG_no_WKT",
            "GeoGraphRAG_no_Template",
            "GeoGraphRAG_no_OOD"
        ]

        for model_data in generation_data:
            model_name = model_data['model']
            logging.info(f"🧐 Оценка модели: {model_name}")
            
            safe_model_name = model_name.replace(":", "_")
            
            for item in tqdm(model_data['metrics'], desc=f"Judging {model_name}"):
                query_id = str(item.get('query_id'))
                query = queries_map.get(query_id, "Unknown query")
                category = item.get('category')
                
                ground_truth_item = next((g for g in ground_truth if str(g.get("id")) == query_id), {})
                expected_entities = ground_truth_item.get("expected_entities", [])
                
                for m in modes:
                    if m not in item: continue
                    
                    # Логика оценки аномальных (Out-of-Domain) запросов
                    if category == "anomalous":
                        success = False
                        if m in ["GeoGraphRAG", "GeoGraphRAG_no_CDA", "GeoGraphRAG_no_WKT", "GeoGraphRAG_no_Template", "GeoGraphRAG_no_OOD"]:
                            triples_count = item[m].get('triples', 0) if "triples" in item[m] else 0
                            success = (triples_count == 0)
                        else:
                            success = not item[m].get('exec', True)

                        item[m].update({
                            "semantic_score": 5 if success else 1,
                            "structural_score": 5 if success else 1,
                            "faithfulness_score": 5 if success else 1,
                            "spatial_score": 5 if success else 1,
                            "numerical_score": 5 if success else 1,
                            "topological_score": 5 if success else 1,
                            "categorical_score": 5 if success else 1,
                            "reasoning": "Correct OOD rejection" if success else "Failed to reject OOD query and generated hallucination."
                        })
                    else:
                        py_path = os.path.join(RESULTS_DIR, safe_model_name, m, f"{query_id}.py")
                        
                        code_response = ""
                        if os.path.exists(py_path):
                            with open(py_path, 'r', encoding='utf-8') as f:
                                code_response = f.read()
                        else:
                            code_response = "# ОШИБКА: Файл с кодом не был сгенерирован или не найден."
                            
                        exec_status = item[m].get('exec', False)
                        
                        scores = self.evaluate(query, code_response, exec_status, m, expected_entities)
                        item[m].update(scores)

            with open(FINAL_OUTPUT_PATH, 'w', encoding='utf-8') as f:
                json.dump(generation_data, f, ensure_ascii=False, indent=4)

        logging.info(f"✅ Готово! Итоговый научный отчет сохранен: {FINAL_OUTPUT_PATH}")

if __name__ == "__main__":
    EvaluationPipeline().run()