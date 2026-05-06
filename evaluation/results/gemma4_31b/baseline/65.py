import folium
import pandas as pd
import random

def check_water_levels():
    # 1. Исходные данные о датчиках (Координаты примерные для региона)
    sensors_data = [
        {"id": "AKSU_01", "river": "Aksu River", "lat": 43.52, "lon": 79.51, "value": 4.2},
        {"id": "AKSU_02", "river": "Aksu River", "lat": 43.80, "lon": 79.80, "value": -1.0}, # Ошибка: отрицательное значение
        {"id": "BYZHY_01", "river": "Byzhy River", "lat": 44.10, "lon": 78.20, "value": 2.8},
        {"id": "BYZHY_02", "river": "Byzhy River", "lat": 44.30, "lon": 78.40, "value": None}, # Ошибка: отсутствие данных
    ]

    # 2. Логика проверки исправности
    # Критерии: значение должно быть числом и находиться в диапазоне от 0 до 15 метров
    results = []
    malfunctioning_sensors = []

    for sensor in sensors_data:
        val = sensor["value"]
        is_functional = True
        
        if val is None or not isinstance(val, (int, float)) or val < 0 or val > 15:
            is_functional = False
            malfunctioning_sensors.append(f"{sensor['id']} ({sensor['river']})")
        
        results.append({
            **sensor,
            "status": "OK" if is_functional else "Malfunctioning",
            "color": "green" if is_functional else "red"
        })

    # 3. Визуализация на карте
    # Центрируем карту в районе рек
    m = folium.Map(location=[43.9, 78.8], zoom_start=7)

    for res in results:
        folium.Marker(
            location=[res["lat"], res["lon"]],
            popup=f"Sensor: {res['id']}<br>River: {res['river']}<br>Status: {res['status']}<br>Value: {res['value']}",
            icon=folium.Icon(color=res["color"], icon="info-sign")
        ).add_to(m)

    # Сохранение карты строго в файл 65.html
    m.save("65.html")

    # 4. Вывод отчета
    print("--- Отчет по состоянию датчиков уровня воды ---")
    if malfunctioning_sensors:
        print(f"ВНИМАНИЕ! Обнаружены неисправные датчики: {', '.join(malfunctioning_sensors)}")
    else:
        print("Все датчики работают исправно.")
    
    print("\nДетальная таблица:")
    df = pd.DataFrame(results)
    print(df[['id', 'river', 'value', 'status']])

if __name__ == "__main__":
    check_water_levels()