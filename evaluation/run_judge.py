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

# Укажи здесь модель, которая будет выступать судьей
JUDGE_MODEL = "qwen2.5-coder:7b"  # Легковесный и быстрый для оценки

# Жесткая привязка путей к директории скрипта
EVAL_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(EVAL_DIR, "generation_results.json")
FINAL_OUTPUT_PATH = os.path.join(EVAL_DIR, "final_evaluation_results.json")
RESULTS_DIR = os.path.join(EVAL_DIR, "results") # Путь к папке с .py файлами
GROUND_TRUTH_PATH = os.path.join(EVAL_DIR, "ground_truth.json") # Путь к вопросам

import os
import subprocess
import time
import logging

def restart_ollama():
    """Перезапуск Ollama на Windows для очистки VRAM"""
    logging.info("\n🔄 Очистка VRAM: Перезапуск Ollama (Windows)...")
    try:
        # Убиваем все процессы ollama (принудительно /F)
        subprocess.run(["taskkill", "/F", "/IM", "ollama.exe", "/T"], 
                       capture_output=True, check=False)
        
        # Даем системе немного времени на реальную очистку памяти
        time.sleep(5) 
        
        # Запускаем Ollama снова. 
        # Используем Popen, чтобы скрипт не ждал завершения работы Ollama
        subprocess.Popen(["ollama", "serve"], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL,
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
        
        # Ждем, пока сервер поднимется, особенно для тяжелых моделей (70B)
        logging.info("⏳ Ожидание инициализации (15 сек)...")
        time.sleep(15)
        logging.info("✅ Ollama перезапущена, VRAM должна быть пуста.")
        
    except Exception as e:
        logging.error(f"⚠️ Ошибка при перезапуске Ollama: {e}")

class EvaluationPipeline:
    def __init__(self):
        logging.info(f"⚖️ Инициализация судьи {JUDGE_MODEL} (режим 0.0 temp)...")
        # Температура 0.0 для максимально строгого и детерминированного судейства
        self.judge = ChatOllama(model=JUDGE_MODEL, temperature=0.0)

    def _robust_json_parse(self, text):
        """Очистка вывода от <think> и markdown + защита от кривого JSON."""
        try:
            # 1. Убираем блок размышлений <think>
            text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
            
            # 2. Ищем сам JSON
            match = re.search(r'\{.*\}', text, re.DOTALL)
            json_str = match.group(0) if match else text
            
            # 3. Пытаемся распарсить стандартным json (строго)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                # 4. Если JSON сломан (висячие запятые, одинарные кавычки), спасает ast
                try:
                    return ast.literal_eval(json_str)
                except Exception:
                    return None
        except Exception:
            return None

    def evaluate(self, query, code_response, exec_status, mode, expected_entities):
        """Оценка с использованием эталонных сущностей (Ground Truth)."""
        status_msg = "Execution: SUCCESS" if exec_status else "Execution: FAILED"
        
        # Превращаем список эталонных сущностей в строку
        truth_str = ", ".join(expected_entities) if expected_entities else "None specified"
        
        prompt = f"""
        You are a senior geospatial scientist evaluating a GeoGraphRAG system.
        User Query: "{query}"
        Expected Targets: {truth_str}
        Runtime Status: {status_msg}

        Analyze the Python Code and evaluate it on a scale of 1-5 across these 7 dimensions of Geospatial Knowledge:
        1. Spatial Location: Correctness of coordinates and ROI.
        2. Geometric Morphology: Correct application of spatial geometries (e.g., Points, Lines, Polygons, Bounding Boxes) to represent geographic features.
        3. Attribute Characteristics: Correct usage of hydrological properties (water level, flow).
        4. Feature Relationships: Logical interaction between rivers, stations, and basins.
        5. Evolutionary Processes: Handling of temporal data (dates, intervals).
        6. Operational Mechanisms: Correct hydrological logic (e.g., NDVI calculation, slope analysis).
        7. Semantic Understanding: Correct terminology and naming.

        Output strictly JSON:
        {{
            "semantic_score": <average_of_7_dimensions>,
            "structural_score": <1-5_based_on_execution_status>,
            "faithfulness_score": <1-5_based_on_data_usage_accuracy>,
            "dimension_breakdown": {{ "spatial": <int>, "temporal": <int>, "logic": <int> }},
            "reasoning": "<short explanation>"
        }}
        """
        try:
            res = self.judge.invoke(prompt)
            parsed = self._robust_json_parse(res.content)
            
            if parsed and all(k in parsed for k in ("semantic_score", "structural_score", "faithfulness_score", "reasoning")):
                return parsed
            else:
                return {
                    "semantic_score": 0, "structural_score": 0, "faithfulness_score": 0,
                    "reasoning": "Judge failed to output valid JSON format."
                }
        except Exception as e:
            logging.error(f"Ошибка судьи: {e}")
            return {
                "semantic_score": 0, "structural_score": 0, "faithfulness_score": 0,
                "reasoning": f"Judge error: {str(e)}"
            }

    def run(self):
        if not os.path.exists(INPUT_PATH):
            logging.error(f"❌ Файл {INPUT_PATH} не найден. Сначала запусти run_generation.py")
            return
        if not os.path.exists(GROUND_TRUTH_PATH):
            logging.error(f"❌ Файл {GROUND_TRUTH_PATH} не найден.")
            return

        # 1. Читаем результаты генерации
        with open(INPUT_PATH, 'r', encoding='utf-8') as f:
            generation_data = json.load(f)

        # 2. Читаем оригинальные вопросы из эталона
        with open(GROUND_TRUTH_PATH, 'r', encoding='utf-8') as f:
            ground_truth = json.load(f)
            
        # 3. Создаем словарь для быстрого поиска
        queries_map = {str(item.get("id")): item.get("query") for item in ground_truth}

        # Маппинг для названий папок на диске
        folder_map = {
            'Baseline': 'baseline', 
            'VectorRAG': 'vector_rag', 
            'GeoGraphRAG': 'geographrag'
        }

        eval_counter = 0  # Счетчик для очистки VRAM

        for model_data in generation_data:
            model_name = model_data['model']
            logging.info(f"🧐 Оценка модели: {model_name}")
            
            safe_model_name = model_name.replace(":", "_")
            
            for item in tqdm(model_data['metrics'], desc=f"Judging {model_name}"):
                
                # --- БЛОК ОЧИСТКИ ПАМЯТИ ---
                eval_counter += 1
                if eval_counter % 50 == 0:  # Каждые 50 вопросов
                    restart_ollama()
                    # Переподключаем LangChain-клиент, чтобы сбросить зависшие HTTP-сессии
                    self.judge = ChatOllama(model=JUDGE_MODEL, temperature=0.0)
                # ------------------------------

                query_id = str(item.get('query_id'))
                query = queries_map.get(query_id, "Unknown query")
                category = item.get('category')
                
                # Достаем эталонные сущности для текущего вопроса
                ground_truth_item = next((g for g in ground_truth if str(g.get("id")) == query_id), {})
                expected_entities = ground_truth_item.get("expected_entities", [])
                
                modes = ['Baseline', 'VectorRAG', 'GeoGraphRAG']
                
                for m in modes:
                    if m not in item: continue
                    
                    # Логика оценки аномальных (Out-of-Domain) запросов
                    if category == "anomalous":
                        # Если GeoGraphRAG не нашел триплетов
                        triples_count = item[m].get('triples', 0) if m == 'GeoGraphRAG' else 0
                        success = (m == 'GeoGraphRAG' and triples_count == 0)
                        
                        item[m].update({
                            "semantic_score": 5 if success else 1,
                            "structural_score": 5 if success else 1,
                            "faithfulness_score": 5 if success else 1,
                            "reasoning": "Correct OOD rejection" if success else "Failed to reject OOD query and generated hallucination."
                        })
                    else:
                        # 1. Формируем путь к .py файлу
                        mode_folder = folder_map.get(m)
                        py_path = os.path.join(RESULTS_DIR, safe_model_name, mode_folder, f"{query_id}.py")
                        
                        # 2. Читаем код из файла
                        code_response = ""
                        if os.path.exists(py_path):
                            with open(py_path, 'r', encoding='utf-8') as f:
                                code_response = f.read()
                        else:
                            code_response = "# ОШИБКА: Файл с кодом не был сгенерирован или не найден."
                            
                        # 3. Берем статус выполнения
                        exec_status = item[m].get('exec', False)
                        
                        # 4. Отправляем судье ВМЕСТЕ с expected_entities
                        scores = self.evaluate(query, code_response, exec_status, m, expected_entities)
                        item[m].update(scores)

            # Сохраняем после оценки каждой модели
            with open(FINAL_OUTPUT_PATH, 'w', encoding='utf-8') as f:
                json.dump(generation_data, f, ensure_ascii=False, indent=4)

        logging.info(f"✅ Готово! Итоговый научный отчет сохранен: {FINAL_OUTPUT_PATH}")

if __name__ == "__main__":
    EvaluationPipeline().run()