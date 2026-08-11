import os
import re
import json
import pandas as pd
from pathlib import Path
from shapely import wkt

# --- НАСТРОЙКИ ---
GT_PATH = "ground_truth.json"
RESULTS_DIR = "results"

# Пункт 18: Исправлена регулярка (внешняя группа ловит весь WKT, внутренняя non-capturing)
WKT_RE = re.compile(
    r"""['"]?((?:POINT|LINESTRING|POLYGON|MULTIPOINT|MULTILINESTRING)\s*\([\d\s.,-]+\))['"]?""",
    re.IGNORECASE
)

def analyze_faithfulness():
    print(f"🚀 Начинаю аудит пространственных галлюцинаций (Frozen Benchmark Mode)...")
    
    if not os.path.exists(GT_PATH):
        print("❌ Файл ground_truth.json не найден!")
        return

    # Читаем эталонные WKT прямо из нашего идеального датасета (Без SPARQL!)
    with open(GT_PATH, 'r', encoding='utf-8') as f:
        raw_gt = json.load(f)
        # Словарь: ID запроса -> список правильных WKT координат
        gt_lookup_wkt = {str(item.get('id')): item.get('expected_wkt', []) for item in raw_gt}

    analysis_results = []
    
    # Считаем общее кол-во файлов для прогресса
    all_files = []
    for root, _, files in os.walk(RESULTS_DIR):
        for f in files:
            if f.endswith(".py"):
                all_files.append(os.path.join(root, f))
    
    total = len(all_files)
    if total == 0:
        print("⚠️ Нет данных для анализа. Запусти run_generation.py.")
        return
        
    print(f"📦 Всего сгенерированных .py файлов для проверки: {total}")

    for idx, file_path in enumerate(all_files):
        path_parts = Path(file_path).parts
        try:
            # Структура пути: ... / Model / Mode / ID.py
            model = path_parts[-3] 
            mode = path_parts[-2]
            q_id = os.path.splitext(path_parts[-1])[0]
        except Exception: 
            continue

        with open(file_path, 'r', encoding='utf-8') as f:
            script_content = f.read()

        # 1. Извлекаем сгенерированные моделью WKT координаты
        found_wkts = WKT_RE.findall(script_content)
        
        # 2. Берем эталонные координаты из Ground Truth
        reference_wkts = gt_lookup_wkt.get(q_id, [])

        # 3. Сверка (Пространственный аудит)
        if not found_wkts:
            # Если WKT нет в коде, и в эталоне их тоже нет -> 1.0 (все верно)
            # Если в коде нет, а в эталоне есть -> 0.0 (галлюцинация упущения)
            score = 1.0 if not reference_wkts else 0.0
        else:
            valid_hits = 0
            for f_wkt_str in found_wkts:
                try:
                    f_geom = wkt.loads(f_wkt_str.strip("'\""))
                    # Проверяем, совпадает ли сгенерированная геометрия с любой из эталонных
                    if any(f_geom.equals(wkt.loads(r)) for r in reference_wkts if r):
                        valid_hits += 1
                except Exception: 
                    continue
            # Доля правильных координат от всех сгенерированных
            score = valid_hits / len(found_wkts)

        analysis_results.append({
            "Architecture": mode, 
            "Model": model, 
            "Spatial_Faithfulness": score
        })

    # Итог
    df = pd.DataFrame(analysis_results)
    report = df.groupby(["Architecture", "Model"])["Spatial_Faithfulness"].mean().reset_index()
    report["Hallucination_Rate"] = 1.0 - report["Spatial_Faithfulness"]
    
    print("\n🏁 ФИНАЛЬНЫЙ ОТЧЕТ (Пространственные Галлюцинации):")
    print(report.round(3).to_string(index=False))
    report.to_csv("spatial_faithfulness_final.csv", index=False)
    print("✅ Результаты сохранены в spatial_faithfulness_final.csv")

if __name__ == "__main__":
    analyze_faithfulness()