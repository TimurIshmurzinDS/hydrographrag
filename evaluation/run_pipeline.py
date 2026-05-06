import subprocess
import sys
import time
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# Список скриптов в строгом порядке выполнения
PIPELINE = [
   # {"file": "download_models.py", "desc": "1. Загрузка/проверка LLM моделей"},
    #{"file": "generate_dataset.py", "desc": "2. Генерация Ground Truth датасета"},
    #{"file": "run_generation.py",   "desc": "3. Ablation Study (Генерация ответов и кода)"},
   {"file": "run_judge.py",        "desc": "4. Оценка судьей (LLM-as-a-Judge)"}
]

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

        process = subprocess.run([sys.executable, script_name], check=True, env=env)
        
        elapsed_time = time.time() - start_time
        mins, secs = divmod(elapsed_time, 60)
        logging.info(f"✅ УСПЕХ: {script_name} завершен за {int(mins)}м {int(secs)}с.\n")
        return True
        
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ ФАТАЛЬНАЯ ОШИБКА: Скрипт {script_name} упал с кодом {e.returncode}.")
        logging.error("🛑 Остановка всего пайплайна, чтобы не испортить данные.")
        return False
    except FileNotFoundError:
        logging.error(f"❌ ОШИБКА: Файл {script_name} не найден в текущей директории.")
        return False

def main():
    logging.info("🌟 Инициализация главного оркестратора GeoGraphRAG...")
    total_start_time = time.time()
    
    for step in PIPELINE:
        success = run_script(step["file"], step["desc"])
        if not success:
            sys.exit(1)
            
    total_time = time.time() - total_start_time
    hours, rem = divmod(total_time, 3600)
    mins, secs = divmod(rem, 60)
    
    logging.info(f"{'='*60}")
    logging.info(f"🎉 ПАЙПЛАЙН ПОЛНОСТЬЮ ЗАВЕРШЕН!")
    logging.info(f"Общее время работы: {int(hours)}ч {int(mins)}м {int(secs)}с.")
    logging.info("Итоговый отчет лежит в 'final_evaluation_results.json'.")
    logging.info(f"{'='*60}")

if __name__ == "__main__":
    main()