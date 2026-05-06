import json
import os

# Имя твоего файла с результатами
FILE_NAME = 'final_evaluation_results.json' 

def fix_json_categories(filename):
    if not os.path.exists(filename):
        print(f"❌ Файл {filename} не найден.")
        return

    print(f"📖 Читаю {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    count = 0
    # Проходим по всей структуре JSON
    for run in data:
        if 'metrics' in run:
            for metric in run['metrics']:
                # Исправляем опечатки в категории
                # Добавляй сюда другие варианты, если они появятся
                if metric.get('category') in ['anomalulus', 'anomalus', 'anomaluous']:
                    metric['category'] = 'anomalous'
                    count += 1

    # Сохраняем обратно
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"✅ Готово! Исправлено вхождений: {count}")
    print(f"💾 Файл {filename} обновлен.")

if __name__ == "__main__":
    fix_json_categories(FILE_NAME)