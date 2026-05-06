import json
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

# Имя твоего файла
RESULTS_FILE = "generation_results.json" 

def post_process_metrics():
    try:
        # Python без проблем прочитает хоть миллион строк за секунды
        with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
            results_data = json.load(f)
    except Exception as e:
        logging.error(f"❌ Ошибка загрузки: {e}")
        return

    print("\n" + "="*70)
    print("📊 ФИНАЛЬНЫЕ МЕТРИКИ ДЛЯ ПРЕДЗАЩИТЫ (Исправленные)")
    print("="*70)

    for model_data in results_data:
        model_name = model_data.get("model")
        metrics = model_data.get("metrics", [])
        
        if not metrics:
            continue

        precisions, recalls, f1_scores = [], [], []
        
        # Статистика генерации кода для Ablation Study
        stats = {
            "Baseline": {"syntax_ok": 0, "map_ok": 0, "total": 0},
            "VectorRAG": {"syntax_ok": 0, "map_ok": 0, "total": 0},
            "GeoGraphRAG": {"syntax_ok": 0, "map_ok": 0, "total": 0}
        }

        for item in metrics:
            # 1. Подсчет успешности написания кода
            for mode in ["Baseline", "VectorRAG", "GeoGraphRAG"]:
                if mode in item:
                    stats[mode]["total"] += 1
                    if item[mode].get("syntax"): stats[mode]["syntax_ok"] += 1
                    if item[mode].get("has_map"): stats[mode]["map_ok"] += 1

            # 2. Подсчет честных метрик Ретривера
            geographrag = item.get("GeoGraphRAG", {})
            retrieval = geographrag.get("retrieval")
            triples_count = geographrag.get("triples", 0)
            
            if retrieval and retrieval.get("status") != "no_ground_truth":
                tp = retrieval.get("targets_found", 0)
                
                # Recall (Target Discovery Rate)
                recall = retrieval.get("tdr", 0.0)
                recalls.append(recall)
                
                # Честный Precision (Context Density)
                if triples_count > 0:
                    precision = min(tp / triples_count, 1.0)
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
        print("-" * 55)
        print("1. Метрики извлечения подграфа (GeoGraphRAG):")
        print(f"   Precision (Плотность контекста) : {avg(precisions):.4f}")
        print(f"   Recall (Полнота нахождения)     : {avg(recalls):.4f}")
        print(f"   F1-Score (Баланс)               : {avg(f1_scores):.4f}")
        
        print("\n2. Способность сгенерировать карту (Ablation Study):")
        for mode in ["Baseline", "VectorRAG", "GeoGraphRAG"]:
            s = stats[mode]
            syn_pct = pct(s['syntax_ok'], s['total'])
            map_pct = pct(s['map_ok'], s['total'])
            print(f"   [{mode.ljust(11)}] Код без ошибок: {syn_pct:5.1f}% | Карта создана: {map_pct:5.1f}%")

    print("\n" + "="*70)

if __name__ == "__main__":
    post_process_metrics()