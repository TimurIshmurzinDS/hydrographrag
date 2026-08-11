import os
import sys
import json
import time
import subprocess
import logging
import hashlib
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# Пункт 34: Полный пайплайн
PIPELINE = [
    {"file": "run_generation.py",          "desc": "1. Ablation Study & Graph Retrieval (Clean Run)"},
    {"file": "run_judge.py",               "desc": "2. Оценка судьей (LLM-as-a-Judge)"},
    {"file": "ood_metrics.py",             "desc": "3. Расчет метрик безопасности (OOD/FRR/FAR)"},
    {"file": "testingforhalliculation.py", "desc": "4. Аудит пространственных галлюцинаций (WKT)"},
    {"file": "analyser_metrics.py",        "desc": "5. Агрегация ретривера и финальный экспорт CSV"}
]

REQUIRED_FIELDS = [
    "id", "query", "category", "expected_behavior", "expected_entities",
    "expected_relations", "expected_triples", "expected_wkt", 
    "expected_numeric_facts", "expected_temporal_facts", 
    "expected_categories", "expected_topology"
]

def calculate_hash(filepath):
    """Считает SHA-256 хэш файла для замороженного бенчмарка"""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def validate_environment_and_dataset():
    """Пункт 35: Строгая предварительная проверка перед долгим запуском"""
    logging.info("🛡️ Запуск обязательной проверки целостности (Validation Check)...")
    
    # 1. Проверяем манифест моделей
    if not os.path.exists("model_manifest.csv"):
        raise FileNotFoundError("❌ Ошибка: файл 'model_manifest.csv' отсутствует!")
    
    # 2. Проверяем ground truth
    gt_path = "ground_truth.json"
    if not os.path.exists(gt_path):
        raise FileNotFoundError(f"❌ Ошибка: Файл {gt_path} отсутствует!")
        
    with open(gt_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
        
    if len(dataset) != 285:
        raise ValueError(f"❌ Ошибка: Ожидалось ровно 285 запросов, найдено {len(dataset)}!")
        
    counts = {"explicit": 0, "semi-explicit": 0, "implicit": 0, "anomalous": 0}
    for i, item in enumerate(dataset):
        cat = item.get("category")
        if cat not in counts:
            raise ValueError(f"❌ Неизвестная категория '{cat}' в записи ID {item.get('id')}!")
        counts[cat] += 1
        
        # Проверяем наличие всех 12 золотых полей
        missing = [f for f in REQUIRED_FIELDS if f not in item]
        if missing:
            raise ValueError(f"❌ Запись ID {item.get('id')} не имеет обязательных полей: {missing}")

    expected_counts = {"explicit": 60, "semi-explicit": 67, "implicit": 83, "anomalous": 75}
    for cat, expected in expected_counts.items():
        if counts[cat] != expected:
            raise ValueError(f"❌ Ошибка квот: '{cat}' = {counts[cat]} (ожидалось {expected})!")
            
    logging.info("✅ Валидация пройдена: Датасет заморожен и структура идеальна.")
    return calculate_hash(gt_path)

def generate_benchmark_manifest(gt_hash):
    """Создаем итоговый манифест бенчмарка для ревьюера (Пункт 39)"""
    manifest_path = "benchmark_manifest.csv"
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write("Field,Value\n")
        f.write(f"Benchmark_Name,HydroGraphRAG_Frozen_Benchmark\n")
        f.write(f"Dataset_Size,285\n")
        f.write(f"Explicit,60\n")
        f.write(f"Semi_Explicit,67\n")
        f.write(f"Implicit,83\n")
        f.write(f"Anomalous,75\n")
        f.write(f"Seed,42\n")
        f.write(f"Temperature,0.0\n")
        f.write(f"Generator_Models,7\n")
        f.write(f"Judge_Model,qwen2.5:72b-instruct\n")
        f.write(f"Dataset_SHA256,{gt_hash}\n")
        f.write(f"Timestamp,{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    logging.info(f"✅ Создан {manifest_path}")

def run_script(script_name, description):
    logging.info(f"{'='*60}")
    logging.info(f"🚀 СТАРТ: {description} ({script_name})")
    
    start_time = time.time()
    try:
        env = os.environ.copy()
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        env["PYTHONPATH"] = project_root + os.pathsep + env.get("PYTHONPATH", "")

        subprocess.run([sys.executable, script_name], check=True, env=env)
        
        elapsed_time = time.time() - start_time
        mins, secs = divmod(elapsed_time, 60)
        logging.info(f"✅ УСПЕХ: завершено за {int(mins)}м {int(secs)}с.\n")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ ФАТАЛЬНАЯ ОШИБКА в {script_name}. Код: {e.returncode}")
        return False

def main():
    logging.info("🌟 Инициализация главного оркестратора HydroGraphRAG...")
    
    try:
        gt_hash = validate_environment_and_dataset()
    except Exception as e:
        logging.error(str(e))
        sys.exit(1)
    
    total_start_time = time.time()
    
    for step in PIPELINE:
        if not run_script(step["file"], step["desc"]):
            sys.exit(1)
            
    generate_benchmark_manifest(gt_hash)
            
    total_time = time.time() - total_start_time
    hours, rem = divmod(total_time, 3600)
    mins, secs = divmod(rem, 60)
    
    logging.info(f"{'='*60}")
    logging.info(f"🎉 ПОЛНЫЙ НАУЧНЫЙ ПАЙПЛАЙН УСПЕШНО ЗАВЕРШЕН!")
    logging.info(f"Общее время работы: {int(hours)}ч {int(mins)}м {int(secs)}с.")
    logging.info("Все итоговые таблицы сгенерированы! Вы великолепны.")
    logging.info(f"{'='*60}")

if __name__ == "__main__":
    main()