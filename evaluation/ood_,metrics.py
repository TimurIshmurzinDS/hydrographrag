import json
import pandas as pd
import os

RESULTS_PATH = "generation_results.json"
RESULTS_DIR = "results"

def calculate_ood_metrics():
    print("📊 Расчет метрик OOD (Abstention Policy)...\n")
    
    with open(RESULTS_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    architectures = ["Baseline", "VectorRAG", "GeoGraphRAG"]
    metrics_list = []

    for run in data:
        model_name = run.get("model", "unknown")
        
        # Счетчики для каждой архитектуры
        stats = {arch: {"TP": 0, "FP": 0, "TN": 0, "FN": 0} for arch in architectures}
        
        for metric in run.get("metrics", []):
            query_id = str(metric.get("query_id"))
            category = metric.get("category", "unknown").lower()
            is_gt_anomalous = "anomal" in category
            
            for arch in architectures:
                if arch not in metric: continue
                
                # Читаем сгенерированный код, чтобы проверить, был ли отказ
                safe_model_name = model_name.replace(":", "_")
                folder_map = {'Baseline': 'baseline', 'VectorRAG': 'vector_rag', 'GeoGraphRAG': 'geographrag'}
                py_path = os.path.join(RESULTS_DIR, safe_model_name, folder_map[arch], f"{query_id}.py")
                
                model_rejected = False
                if os.path.exists(py_path):
                    with open(py_path, 'r', encoding='utf-8') as f:
                        code_content = f.read()
                        # Ищем ключевую фразу отказа из единого шаблона
                        if "ОТКАЗ: Запрос не относится" in code_content:
                            model_rejected = True

                # Матрица ошибок
                if is_gt_anomalous and model_rejected:
                    stats[arch]["TP"] += 1  # Верно отклонил мусор
                elif is_gt_anomalous and not model_rejected:
                    stats[arch]["FN"] += 1  # Сгенерировал галлюцинацию на мусор
                elif not is_gt_anomalous and model_rejected:
                    stats[arch]["FP"] += 1  # Ложно отклонил хороший запрос
                elif not is_gt_anomalous and not model_rejected:
                    stats[arch]["TN"] += 1  # Верно ответил на хороший запрос

        # Расчет метрик
        for arch in architectures:
            s = stats[arch]
            tp, fp, tn, fn = s["TP"], s["FP"], s["TN"], s["FN"]
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
            frr = fp / (fp + tn) if (fp + tn) > 0 else 0.0  # False Rejection Rate
            
            metrics_list.append({
                "Model": model_name,
                "Architecture": arch,
                "OOD_Precision": round(precision, 3),
                "OOD_Recall": round(recall, 3),
                "OOD_F1_Score": round(f1, 3),
                "False_Rejection_Rate": round(frr, 3)
            })

    df = pd.DataFrame(metrics_list)
    
    print("🏆 Сводная таблица OOD метрик:")
    # Усредняем по всем моделям
    summary = df.groupby('Architecture')[["OOD_Precision", "OOD_Recall", "OOD_F1_Score", "False_Rejection_Rate"]].mean().round(3)
    print(summary.to_string())
    
    df.to_csv("ood_metrics_detailed.csv", index=False)
    summary.to_csv("ood_metrics_summary.csv")
    print("\n✅ Сохранено в ood_metrics_summary.csv")

if __name__ == "__main__":
    calculate_ood_metrics()