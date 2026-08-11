import json

def normalize_dataset():
    input_file = "ground_truth.json"
    output_file = "ground_truth_normalized.json"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    normalized_data = []
    counts = {"explicit": 0, "semi-explicit": 0, "implicit": 0, "anomalous": 0}

    for idx, item in enumerate(data):
        new_item = {}
        
        # 1. Базовые поля
        new_item["id"] = item.get("id", idx + 1)
        new_item["query"] = item.get("query", "")
        
        # 2. Исправление опечаток и категорий (Пункты 21, 22)
        cat = item.get("category", "").lower().strip()
        if cat == "anomalulus" or cat == "ood":
            cat = "anomalous"
            
        # Ручная корректировка сбившихся категорий (Пункт 21)
        # Если есть запросы 129-135, которые должны быть implicit, а стоят semi-explicit
        if 129 <= new_item["id"] <= 135:
            cat = "implicit"
            
        new_item["category"] = cat

        # 3. Ожидаемое поведение
        new_item["expected_behavior"] = "reject" if cat == "anomalous" else "generate_code"

        # 4. Расширение до полного графа (Пункт 20)
        # Сохраняем старые данные, если есть, иначе пустой список
        new_item["expected_entities"] = item.get("expected_entities", [])
        new_item["expected_relations"] = item.get("expected_relations", [])
        new_item["expected_triples"] = item.get("expected_triples", [])
        
        # Обработка WKT и чисел (если они раньше назывались по-другому)
        new_item["expected_wkt"] = item.get("expected_wkt", [])
        numeric = item.get("expected_numeric_facts", item.get("expected_values", []))
        new_item["expected_numeric_facts"] = numeric
        
        new_item["expected_temporal_facts"] = item.get("expected_temporal_facts", [])
        new_item["expected_categories"] = item.get("expected_categories", [])
        new_item["expected_topology"] = item.get("expected_topology", [])

        normalized_data.append(new_item)
        if cat in counts:
            counts[cat] += 1

    # Валидация (Пункт 21)
    print(f"📊 Итоговое распределение: {counts}")
    print(f"📦 Всего записей: {len(normalized_data)}")
    
    assert len(normalized_data) == 285, "❌ Ошибка: В датасете не 285 запросов!"
    assert counts["explicit"] == 60, f"❌ Ошибка explicit: {counts['explicit']} != 60"
    assert counts["semi-explicit"] == 67, f"❌ Ошибка semi-explicit: {counts['semi-explicit']} != 67"
    assert counts["implicit"] == 83, f"❌ Ошибка implicit: {counts['implicit']} != 83"
    assert counts["anomalous"] == 75, f"❌ Ошибка anomalous: {counts['anomalous']} != 75"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(normalized_data, f, ensure_ascii=False, indent=4)
        
    print(f"\n✅ Датасет успешно нормализован и сохранен как {output_file}.")
    print("⚠️ Переименуй его обратно в ground_truth.json и больше НИКОГДА не меняй (Пункт 23).")

if __name__ == "__main__":
    normalize_dataset()