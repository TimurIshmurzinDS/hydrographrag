import json
import pandas as pd
import os

# Укажи путь к файлу, который выдал судья (или к generation_results.json)
INPUT_FILE = "final_evaluation_results.json" 
OUTPUT_DIR = "exported_tables"

def extract_tables():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Файл {INPUT_FILE} не найден!")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for model_data in data:
        model_name = model_data.get("model", "unknown_model")
        metrics = model_data.get("metrics", [])
        
        if not metrics:
            continue
            
        print(f"\n🚀 Обработка данных для модели: {model_name}")
        
        perf_rows = []
        judge_rows = []
        retr_rows = []

        for item in metrics:
            q_id = item.get("query_id")
            
            for mode in ["Baseline", "VectorRAG", "GeoGraphRAG"]:
                if mode not in item:
                    continue
                
                m_data = item[mode]
                
                # 1. Таблица производительности
                perf_rows.append({
                    "Query_ID": q_id,
                    "Mode": mode,
                    "Latency (s)": m_data.get("latency"),
                    "Syntax": m_data.get("syntax"),
                    "Exec": m_data.get("exec"),
                    "Has_Map": m_data.get("has_map")
                })
                
                # 2. Таблица оценок судьи
                judge_rows.append({
                    "Query_ID": q_id,
                    "Mode": mode,
                    "Semantic": m_data.get("semantic_score"),
                    "Structural": m_data.get("structural_score"),
                    "Faithfulness": m_data.get("faithfulness_score")
                })
                
                # 3. Таблица ретривера (только для GeoGraphRAG)
                if mode == "GeoGraphRAG":
                    retr = m_data.get("retrieval", {})
                    retr_rows.append({
                        "Query_ID": q_id,
                        "Triples": m_data.get("triples"),
                        "Precision": retr.get("precision"),
                        "Recall": retr.get("recall"),
                        "F1": retr.get("f1")
                    })

        # Превращаем в DataFrames
        df_perf = pd.DataFrame(perf_rows)
        df_judge = pd.DataFrame(judge_rows)
        df_retr = pd.DataFrame(retr_rows)

        # Сохраняем подробные таблицы в CSV
        safe_model = model_name.replace(":", "_")
        
        df_perf.to_csv(os.path.join(OUTPUT_DIR, f"{safe_model}_performance.csv"), index=False)
        df_judge.to_csv(os.path.join(OUTPUT_DIR, f"{safe_model}_judge.csv"), index=False)
        if not df_retr.empty:
            df_retr.to_csv(os.path.join(OUTPUT_DIR, f"{safe_model}_retrieval.csv"), index=False)

        # --- 4. СОЗДАЕМ СВОДНУЮ ТАБЛИЦУ (АГРЕГАЦИЯ) ---
        summary = []
        for mode in ["Baseline", "VectorRAG", "GeoGraphRAG"]:
            mode_perf = df_perf[df_perf["Mode"] == mode]
            mode_judge = df_judge[df_judge["Mode"] == mode]
            
            if len(mode_perf) == 0:
                continue

            exec_rate = mode_perf["Exec"].fillna(False).mean() * 100
            map_rate = mode_perf["Has_Map"].fillna(False).mean() * 100
            avg_lat = mode_perf["Latency (s)"].mean()
            
            avg_sem = mode_judge["Semantic"].mean()
            avg_str = mode_judge["Structural"].mean()
            avg_fai = mode_judge["Faithfulness"].mean()
            
            # Для Recall берем из ретривера, если это GeoGraphRAG
            avg_recall = df_retr["Recall"].mean() if mode == "GeoGraphRAG" and not df_retr.empty else None
            
            summary.append({
                "Mode": mode,
                "Exec Rate (%)": round(exec_rate, 1),
                "Map Rate (%)": round(map_rate, 1),
                "Avg Latency (s)": round(avg_lat, 2),
                "Avg Semantic": round(avg_sem, 2) if pd.notnull(avg_sem) else None,
                "Avg Structural": round(avg_str, 2) if pd.notnull(avg_str) else None,
                "Avg Faithfulness": round(avg_fai, 2) if pd.notnull(avg_fai) else None,
                "Avg Recall": round(avg_recall, 2) if avg_recall is not None else "N/A"
            })
        
        df_summary = pd.DataFrame(summary)
        summary_path = os.path.join(OUTPUT_DIR, f"{safe_model}_SUMMARY.csv")
        df_summary.to_csv(summary_path, index=False)
        
        print("\n📊 СВОДНАЯ ТАБЛИЦА (Уже сохранена в Excel/CSV):")
        print(df_summary.to_markdown(index=False))
        print(f"\n✅ Все файлы сохранены в папку: {os.path.abspath(OUTPUT_DIR)}")
        print("-" * 60)

if __name__ == "__main__":
    extract_tables()