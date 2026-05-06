import folium
import pandas as pd
from datetime import datetime

def get_latest_water_level(river_name):
    """
    Симуляция функции получения данных из API гидрологической службы.
    В реальном сценарии здесь будет запрос requests.get(url).
    """
    # Имитация базы данных гидропостов
    mock_db = {
        "Talgar River": {
            "coords": [43.2150, 77.2310], 
            "readings": [
                {"timestamp": "2023-10-25 10:00", "level": 1.25},
                {"timestamp": "2023-10-26 10:00", "level": 1.32},
                {"timestamp": "2023-10-27 10:00", "level": 1.41}, # Последний показатель
            ]
        },
        "Ili River": {
            "coords": [43.5000, 78.1000],
            "readings": [
                {"timestamp": "2023-10-27 10:00", "level": 3.10},
            ]
        }
    }
    
    if river_name in mock_db:
        data = mock_db[river_name]
        # Получаем последний элемент списка измерений
        latest_record = data["readings"][-1]
        return {
            "coords": data["coords"],
            "level": latest_record["level"],
            "time": latest_record["timestamp"]
        }
    else:
        return None

def main():
    river = "Talgar River"
    print(f"Поиск последнего показателя уровня воды для {river}...")
    
    # 1. Получение данных
    result = get_latest_water_level(river)
    
    if result:
        coords = result["coords"]
        level = result["level"]
        time = result["time"]
        
        print(f"Последний зафиксированный уровень воды: {level} м. (Дата: {time})")
        
        # 2. Создание карты
        # Центрируем карту на координатах реки
        m = folium.Map(location=coords, zoom_start=12, control_scale=True)
        
        # Создание текста для всплывающего окна
        popup_text = f"<b>Река:</b> {river}<br>" \
                     f"<b>Уровень воды:</b> {level} м.<br>" \
                     f"<b>Дата замера:</b> {time}"
        
        # Добавление маркера на карту
        folium.Marker(
            location=coords,
            popup=folium.Popup(popup_text, max_width=300),
            tooltip="Гидрологический пост Talgar River",
            icon=folium.Icon(color='blue', icon='tint')
        ).add_to(m)
        
        # 3. Сохранение карты
        m.save("3.html")
        print("Результат визуализации сохранен в файл 3.html")
    else:
        print("Данные по указанной реке не найдены.")

if __name__ == "__main__":
    main()