import os
import re
import json
import pandas as pd
from pathlib import Path
from shapely import wkt
from SPARQLWrapper import SPARQLWrapper, JSON
import functools

# --- НАСТРОЙКИ ---
GT_PATH = "ground_truth.json"
RESULTS_DIR = "results"
SPARQL_ENDPOINT = "http://localhost:7200/repositories/HydroDB"

# Улучшенная регулярка (ловит WKT в любых кавычках и без)
WKT_RE = re.compile(r"['\"]?(POINT|LINESTRING|POLYGON|MULTIPOINT|MULTILINESTRING)\s*\([\d\s.,\-()]+\)['\"]?", re.IGNORECASE)

@functools.lru_cache(maxsize=512)
def fetch_truth_from_db(entity_label):
    """Кэшируемый запрос к базе, чтобы не дергать её по пустякам"""
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    query = f"""
    PREFIX geo: <http://www.opengis.net/ont/geosparql#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?wkt WHERE {{
        ?s rdfs:label "{entity_label}" .
        ?s geo:hasGeometry/geo:asWKT ?wkt .
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        return [b["wkt"]["value"] for b in results["results"]["bindings"]]
    except:
        return []

def analyze_faithfulness():
    print(f"🚀 Начинаю аудит. Ryzen 9700X в деле...")
    
    if not os.path.exists(GT_PATH):
        return print("❌ Файл ground_truth.json не найден!")

    with open(GT_PATH, 'r', encoding='utf-8') as f:
        raw_gt = json.load(f)
        gt_lookup = {str(item.get('id')): item.get('expected_entities', []) for item in raw_gt}

    analysis_results = []
    
    # Считаем общее кол-во файлов для прогресса
    all_files = []
    for root, _, files in os.walk(RESULTS_DIR):
        for f in files:
            if f.endswith(".py"):
                all_files.append(os.path.join(root, f))
    
    total = len(all_files)
    print(f"📦 Всего файлов для проверки: {total}")

    for idx, file_path in enumerate(all_files):
        # Выводим прогресс каждые 50 файлов
        if idx % 50 == 0:
            print(f"⏳ Обработано {idx}/{total} ({round(idx/total*100, 1)}%)...")

        path_parts = Path(file_path).parts
        try:
            # Структура: results/Model/Mode/ID.py
            model = path_parts[1]
            mode = path_parts[2]
            q_id = os.path.splitext(path_parts[3])[0]
        except: continue

        with open(file_path, 'r', encoding='utf-8') as f:
            script_content = f.read()

        # 1. Извлекаем WKT
        found_wkts = WKT_RE.findall(script_content)
        
        # 2. Ищем эталон
        expected_names = gt_lookup.get(q_id, [])
        reference_wkts = []
        for name in expected_names:
            reference_wkts.extend(fetch_truth_from_db(name))

        # 3. Сверка
        if not found_wkts:
            score = 1.0 if not expected_names else 0.0
        else:
            valid_hits = 0
            for f_wkt_str in found_wkts:
                try:
                    f_geom = wkt.loads(f_wkt_str.strip("'\""))
                    if any(f_geom.equals(wkt.loads(r)) for r in reference_wkts if r):
                        valid_hits += 1
                except: continue
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
    
    print("\n🏁 ФИНАЛЬНЫЙ ОТЧЕТ:")
    print(report.round(3).to_string(index=False))
    report.to_csv("spatial_faithfulness_final.csv", index=False)

if __name__ == "__main__":
    analyze_faithfulness()