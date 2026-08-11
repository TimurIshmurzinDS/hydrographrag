import os
import sys
import json
import time
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# Полная цепочка скриптов для научных расчетов (включая все новые метрики)
PIPELINE = [
    {"file": "run_generation.py",          "desc": "1. Ablation Study (Генерация ответов и кода)"},
    {"file": "run_judge.py",               "desc": "2. Оценка судьей (LLM-as-a-Judge)"},
    {"file": "ood_metrics.py",             "desc": "3. Расчет детальных OOD-метрик (TP/FP/TN/FN)"},
    {"file": "testingforhalliculation.py",  "desc": "4. Аудит пространственных галлюцинаций (WKT)"},
    {"file": "analyser_metrics.py",        "desc": "5. Метрики ретривера и финальная агрегация"}
]

def validate_environment_and_dataset():
    """Предохранитель (Пункты 37, 38): строгая проверка перед запуском"""
    logging.info("🛡️ Запуск обязательной проверки целостности (Validation Check)...")
    
    # 1. Проверяем наличие файла манифеста моделей
    if not os.path.exists("model_manifest.csv"):
        logging.warning("⚠️ Внимание: файл 'model_manifest.csv' не найден. Убедитесь, что добавили его для ревьюера.")
    
    # 2. Проверяем замороженный датасет
    gt_path = "ground_truth.json"
    if not os.path.exists(gt_path):
        raise FileNotFoundError(f"❌ Фатальная ошибка: Файл {gt_path} отсутствует!")
        
    with open(gt_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
        
    # Проверка длины (строго 285)
    if len(dataset) != 285:
        raise ValueError(f"❌ Ошибка валидации: Ожидалось ровно 285 запросов, а найдено {len(dataset)}!")
        
    # Проверка распределения категорий (60 / 67 / 83 / 75)
    counts = {"explicit": 0, "semi-explicit": 0, "implicit": 0, "anomalous": 0}
    for item in dataset:
        cat = item.get("category")
        if cat in counts:
            counts[cat] += 1
            
    expected_counts = {"explicit": 60, "semi-explicit": 67, "implicit": 83, "anomalous": 75}
    for cat, expected in expected_counts.items():
        if counts[cat] != expected:
            raise ValueError(f"❌ Ошибка валидации категорий: в '{cat}' получено {counts[cat]} (ожидалось {expected})!")
            
    logging.info("✅ Валидация успешна: Датасет заморожен, структура корректна, параметры соблюдены.")

def run_script(script_name, description):
    logging.info(f"{'='*60}")
    logging.info(f"🚀 СТАРТ: {description} ({script_name})")
    logging.info(f"{'='*60}")
    
    start_time = time.time()
    try:
        # МАГИЯ ЗДЕСЬ: Добавляем корневую папку (Code) в пути видимости Python
        env = os.environ.copy()
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        env["PYTHONPATH"] = project_root + os.pathsep + env.get("PYTHONPATH", "")

        subprocess.run([sys.executable, script_name], check=True, env=env)
        
        elapsed_time = time.time() - start_time
        mins, secs = divmod(elapsed_time, 60)
        logging.info(f"✅ УСПЕХ: {script_name} завершен за {int(mins)}м {int(secs)}с.\n")
        return True
        
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ ФАТАЛЬНАЯ ОШИБКА: Скрипт {script_name} упал с кодом {e.returncode}.")
        logging.error("🛑 Прерывание пайплайна во избежание порчи результатов.")
        return False
    except FileNotFoundError:
        logging.error(f"❌ ОШИБКА: Файл {script_name} не найден в текущей директории.")
        return False

def main():
    logging.info("🌟 Инициализация главного оркестратора HydroGraphRAG...")
    
    # Сначала выполняем валидацию, если она падает — скрипт завершается
    try:
        validate_environment_and_dataset()
    except Exception as e:
        logging.error(str(e))
        sys.exit(1)
    
    total_start_time = time.time()
    
    for step in PIPELINE:
        success = run_script(step["file"], step["desc"])
        if not success:
            sys.exit(1)
            
    total_time = time.time() - total_start_time
    hours, rem = divmod(total_time, 3600)
    mins, secs = divmod(rem, 60)
    
    logging.info(f"{'='*60}")
    logging.info(f"🎉 ПОЛНЫЙ НАУЧНЫЙ ПАЙПЛАЙН УСПЕШНО ЗАВЕРШЕН!")
    logging.info(f"Общее время работы: {int(hours)}ч {int(mins)}м {int(secs)}с.")
    logging.info("Все итоговые метрики и таблицы сгенерированы автоматически.")
    logging.info(f"{'='*60}")

if __name__ == "__main__":
    main()