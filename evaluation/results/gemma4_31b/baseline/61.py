import folium
import pandas as pd
import random

# 1. Симуляция данных датчиков уровня воды на реке Aksu
# Координаты примерно соответствуют региону реки Aksu (Центральная Азия)
data = {
    'sensor_id': [f'SN_{i}' for i in range(1, 11)],
    'lat': [42.85, 42.92, 43.01, 43.15, 43.28, 43.40, 43.55, 43.70, 43.85, 44.00],
    'lon': [80.10, 80.25, 80.40, 80.55, 80.70, 80.85, 81.00, 81.15, 81.30, 81.45],
    'water_level': [1.2, 1.5, 2.8, 0.9, 3.1, 1.1, 0.0, 1.4, 2.9, 1.0],
    'status': ['Active', 'Active', 'Warning', 'Active', 'Warning', 'Active', 'Inactive', 'Active', 'Active', 'Inactive']
}

df = pd.DataFrame(data)

def get_color(status):
    """Определяет цвет маркера в зависимости от статуса датчика"""
    if status == 'Active':
        return 'green'
    elif status == 'Warning':
        return 'orange'
    elif status == 'Inactive':
        return 'red'
    else:
        return 'gray'

# 2. Создание карты
# Центрируем карту на среднем значении координат датчиков
center_lat = df['lat'].mean()
center_lon = df['lon'].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=7, tiles='OpenStreetMap')

# 3. Добавление датчиков на карту
for index, row in df.iterrows():
    # Формируем текст для всплывающего окна
    popup_text = (
        f"Sensor ID: {row['sensor_id']}<br>"
        f"Status: {row['status']}<br>"
        f"Water Level: {row['water_level']} m"
    )
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=popup_text,
        color=get_color(row['status']),
        fill=True,
        fill_color=get_color(row['status']),
        fill_opacity=0.7
    ).add_to(m)

# 4. Сохранение результата
m.save("61.html")

print("Анализ завершен. Карта с итоговым статусом датчиков сохранена в файл 61.html")