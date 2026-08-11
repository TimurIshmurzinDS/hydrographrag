import json
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

# Имя твоего файла с результатами генерации
RESULTS_FILE = "generation_results.json" 

def post_process_metrics():
    try:
        # Читаем JSON с результатами
        with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
            results_data = json.load(f)
    except Exception as e:
        logging.error(f"❌ Ошибка загрузки: {e}")
        return

    print("\n" + "="*70)
    print("📊 ФИНАЛЬНЫЕ МЕТРИКИ (Исправленные для IEEE Access)")
    print("="*70)

    for model_data in results_data:
        model_name = model_data.get("model")
        metrics = model_data.get("metrics", [])
        
        if not metrics:
            continue

        precisions, recalls, f1_scores = [], [], []
        
        # Статистика генерации кода для Ablation Study (Имя заменено на HydroGraphRAG)
        stats = {
            "Baseline": {"syntax_ok": 0, "map_ok": 0, "total": 0},
            "VectorRAG": {"syntax_ok": 0, "map_ok": 0, "total": 0},
            "HydroGraphRAG": {"syntax_ok": 0, "map_ok": 0, "total": 0}
        }

        for item in metrics:
            # 1. Подсчет успешности написания кода
            for mode in ["Baseline", "VectorRAG", "HydroGraphRAG"]:
                if mode in item:
                    stats[mode]["total"] += 1
                    if item[mode].get("syntax"): stats[mode]["syntax_ok"] += 1
                    if item[mode].get("has_map"): stats[mode]["map_ok"] += 1

            # 2. Подсчет честных метрик Ретривера (Entity-level)
            hydrographrag = item.get("HydroGraphRAG", {})
            retrieval = hydrographrag.get("retrieval")
            
            if retrieval and retrieval.get("status") != "no_ground_truth":
                tp = retrieval.get("targets_found", 0)
                # Берем реальное количество извлеченных сущностей, а не триплетов!
                retrieved_entities = retrieval.get("retrieved_total", 0) 
                
                # Recall (Target Discovery Rate)
                recall = retrieval.get("tdr", 0.0)
                recalls.append(recall)
                
                # Честный Entity-level Precision
                if retrieved_entities > 0:
                    precision = min(tp / retrieved_entities, 1.0)
                else:
                    precision = 0.0
                    
                precisions.append(precision)
                
                # F1 Score
                if precision + recall > 0:
                    f1 = 2 * (precision * recall) / (precision + recall)
                else:
                    f1 = 0.0
                f1_scores.append(f1)

        if not precisions:
            continue

        def avg(lst): return sum(lst) / len(lst) if lst else 0.0
        def pct(part, whole): return (part / whole * 100) if whole else 0.0

        print(f"\n🚀 Модель: {model_name}")
        print("-" * 57)
        print("1. Метрики извлечения подграфа (HydroGraphRAG):")
        print(f"   Precision (Entity-level)        : {avg(precisions):.4f}")
        print(f"   Recall (Target Discovery Rate)  : {avg(recalls):.4f}")
        print(f"   F1-Score (Баланс)               : {avg(f1_scores):.4f}")
        
        print("\n2. Способность сгенерировать карту (Ablation Study):")
        for mode in ["Baseline", "VectorRAG", "HydroGraphRAG"]:
            s = stats[mode]
            syn_pct = pct(s['syntax_ok'], s['total'])
            map_pct = pct(s['map_ok'], s['total'])
            print(f"   [{mode.ljust(13)}] Код без ошибок: {syn_pct:5.1f}% | Карта создана: {map_pct:5.1f}%")

    print("\n" + "="*70)

if __name__ == "__main__":
    post_process_metrics()