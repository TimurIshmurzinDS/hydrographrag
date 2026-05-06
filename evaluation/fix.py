import json

def clean_dataset():
    file_path = 'ground_truth.json'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        # Убираем технический мусор из вопроса
        item['query'] = item['query'].replace(' (HY_HydroFeature)', '')
        
        # Убираем из списка ожидаемых сущностей
        if 'expected_entities' in item:
            item['expected_entities'] = [e.replace(' (HY_HydroFeature)', '') for e in item['expected_entities']]
            
        # Убираем из аннотаций (если есть)
        if 'expected_annotated_entities' in item:
            item['expected_annotated_entities'] = [e.replace(' (HY_HydroFeature)', '') for e in item['expected_annotated_entities']]

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print("✅ Датасет успешно очищен от (HY_HydroFeature)!")

if __name__ == "__main__":
    clean_dataset()