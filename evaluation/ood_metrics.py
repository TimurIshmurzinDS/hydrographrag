import json
import pandas as pd
import os

RESULTS_PATH = "generation_results.json"

def calculate_ood_metrics():
    print("📊 Расчет честных OOD метрик (на основе JSON decision)...\n")
    
    if not os.path.exists(RESULTS_PATH):
        print(f"❌ Файл {RESULTS_PATH} не найден.")
        return

    with open(RESULTS_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Пункт 11: Учитываем все 9 архитектур
    # Пункт 10: Используем строго HydroGraphRAG
    architectures = [
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
    
    metrics_list = []

    for run in data:
        model_name = run.get("model", "unknown")
        
        # Матрицы ошибок для текущей модели
        stats = {arch: {"TP": 0, "FP": 0, "TN": 0, "FN": 0} for arch in architectures}
        
        for metric in run.get("metrics", []):
            category = metric.get("category", "unknown").lower()
            is_gt_anomalous = (category == "anomalous")
            
            for arch in architectures:
                if arch not in metric: 
                    continue
                
                # Пункты 3 и 4: Никаких проверок файлов .py или статуса exec.
                # Читаем ТОЛЬКО поле decision, которое вернула модель.
                arch_data = metric[arch]
                decision = str(arch_data.get("decision", "ANSWER")).upper()
                model_rejected = (decision == "ABSTAIN")

                # Матрица ошибок
                if is_gt_anomalous and model_rejected:
                    stats[arch]["TP"] += 1  # Верно отклонил мусор (True Positive for OOD)
                elif is_gt_anomalous and not model_rejected:
                    stats[arch]["FN"] += 1  # Сгенерировал ответ на мусор (False Negative)
                elif not is_gt_anomalous and model_rejected:
                    stats[arch]["FP"] += 1  # Ложно отклонил хороший запрос (False Positive)
                elif not is_gt_anomalous and not model_rejected:
                    stats[arch]["TN"] += 1  # Верно ответил на хороший запрос (True Negative)

        # Пункт 5: Расчет всех запрошенных метрик
        for arch in architectures:
            s = stats[arch]
            tp, fp, tn, fn = s["TP"], s["FP"], s["TN"], s["FN"]
            
            # Базовые
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
            
            # Дополнительные метрики безопасности
            frr = fp / (fp + tn) if (fp + tn) > 0 else 0.0  # False Rejection Rate (ошибочный отказ)
            far = fn / (fn + tp) if (fn + tp) > 0 else 0.0  # False Acceptance Rate (пропуск мусора)
            specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0 # Специфичность
            
            metrics_list.append({
                "Model": model_name,
                "Architecture": arch,
                "TP": tp, "FP": fp, "TN": tn, "FN": fn,
                "OOD_Precision": round(precision, 4),
                "OOD_Recall": round(recall, 4),
                "OOD_F1_Score": round(f1, 4),
                "False_Rejection_Rate": round(frr, 4),
                "False_Acceptance_Rate": round(far, 4),
                "Specificity": round(specificity, 4)
            })

    if not metrics_list:
        print("⚠️ Нет данных для анализа.")
        return

    df = pd.DataFrame(metrics_list)
    df.to_csv("ood_metrics_detailed.csv", index=False)
    
    print("🏆 Сводная таблица OOD метрик (Усреднено по всем LLM):")
    summary = df.groupby('Architecture')[
        ["OOD_Precision", "OOD_Recall", "OOD_F1_Score", "False_Rejection_Rate", "False_Acceptance_Rate"]
    ].mean().round(4)
    
    print(summary.to_string())
    summary.to_csv("ood_metrics_summary.csv")
    print("\n✅ Сохранено в ood_metrics_summary.csv и ood_metrics_detailed.csv")

if __name__ == "__main__":
    calculate_ood_metrics()