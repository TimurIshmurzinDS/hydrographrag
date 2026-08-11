import json
import os
import pandas as pd

# Берем самый полный файл, который появляется после работы Судьи
RESULTS_FILE = "final_evaluation_results.json"
FALLBACK_FILE = "generation_results.json"

def post_process_metrics():
    print("📊 Агрегация финальных метрик для статьи...")
    
    file_to_read = RESULTS_FILE if os.path.exists(RESULTS_FILE) else FALLBACK_FILE
    if not os.path.exists(file_to_read):
        print(f"❌ Файл {file_to_read} не найден.")
        return

    with open(file_to_read, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Пункт 11: Учитываем все 9 архитектур
    architectures = [
        "Baseline", "VectorRAG", "HydroGraphRAG",
        "HydroGraphRAG_no_CDA", "HydroGraphRAG_no_WKT",
        "HydroGraphRAG_no_Template", "HydroGraphRAG_no_OOD",
        "HydroGraphRAG_no_Cache", "HydroGraphRAG_no_Sandbox"
    ]

    retrieval_records = []
    ablation_records = []

    for model_data in data:
        model_name = model_data.get("model", "unknown")
        metrics = model_data.get("metrics", [])
        
        for item in metrics:
            for arch in architectures:
                if arch not in item:
                    continue
                
                arch_data = item[arch]
                
                # 1. Ablation (Способность генерации)
                ablation_records.append({
                    "Model": model_name,
                    "Architecture": arch,
                    "Syntax_OK": 1 if arch_data.get("syntax") else 0,
                    "Exec_OK": 1 if arch_data.get("exec") else 0,
                    "Has_Map": 1 if arch_data.get("has_map") else 0
                })
                
                # 2. Retrieval Metrics (Только для графовых методов, у которых есть поле 'retrieval')
                # Пункт 9: Читаем строго из item[arch]["retrieval"]
                if "retrieval" in arch_data:
                    r = arch_data["retrieval"]
                    retrieval_records.append({
                        "Model": model_name,
                        "Architecture": arch,
                        "Precision": r.get("precision", 0.0),
                        "Recall": r.get("recall", 0.0),
                        "F1": r.get("f1", 0.0),
                        "Targets_Found": r.get("targets_found", 0),
                        "Retrieved_Entities": r.get("retrieved_entities", 0),
                        "Retrieved_Triples": r.get("retrieved_triples", 0)
                    })

    # Сохранение Ablation Summary
    df_abl = pd.DataFrame(ablation_records)
    # Группируем по Архитектуре и Модели, переводим в %
    df_abl_summary = df_abl.groupby(["Architecture", "Model"]).mean() * 100
    df_abl_summary = df_abl_summary.round(2)
    df_abl_summary.to_csv("ablation_summary.csv")
    
    print("\n📈 ABLATION SUMMARY (Успешность выполнения в %):")
    print(df_abl.groupby("Architecture")[["Syntax_OK", "Exec_OK", "Has_Map"]].mean().round(4) * 100)

    # Сохранение Retrieval Metrics
    if retrieval_records:
        df_ret = pd.DataFrame(retrieval_records)
        df_ret_summary = df_ret.groupby(["Architecture", "Model"])[
            ["Precision", "Recall", "F1", "Targets_Found", "Retrieved_Entities", "Retrieved_Triples"]
        ].mean().round(4)
        df_ret_summary.to_csv("retrieval_metrics.csv")
        
        print("\n🔍 RETRIEVAL METRICS (Macro-Average Entity-Level):")
        print(df_ret.groupby("Architecture")[["Precision", "Recall", "F1"]].mean().round(4))
        
    print("\n✅ Метрики агрегированы и сохранены: ablation_summary.csv, retrieval_metrics.csv")

if __name__ == "__main__":
    post_process_metrics()