import pandas as pd
import numpy as np
import folium
from shapely.geometry import Point, LineString

# Предположим, что у нас есть временные ряды уровня воды в формате CSV
# Структура данных: дата, уровень_воды (м)
shilik_data = pd.read_csv('shilik_water_level.csv', parse_dates=['date'])
sharyn_data = pd.read_csv('sharyn_water_level.csv', parse_dates=['date'])

# Определение порогового значения уровня воды для засухи
drought_threshold_shilik = 1.0  # Примерное значение в метрах
drought_threshold_sharyn = 1.2  # Примерное значение в метрах

# Функция для определения периодов засухи
def find_drought_periods(data, threshold):
    droughts = []
    in_drought = False
    start_date = None
    
    for index, row in data.iterrows():
        if row['уровень_воды'] < threshold:
            if not in_drought:
                in_drought = True
                start_date = row['date']
        else:
            if in_drought:
                droughts.append((start_date, row['date']))
                in_drought = False
    
    # Если засуха продолжалась до конца данных
    if in_drought:
        droughts.append((start_date, data.iloc[-1]['date']))
    
    return droughts

# Определение периодов засухи для обеих рек
shilik_drought_periods = find_drought_periods(shilik_data, drought_threshold_shilik)
sharyn_drought_periods = find_drought_periods(sharyn_data, drought_threshold_sharyn)

# Создание карты с использованием folium
m = folium.Map(location=[50.1296, 83.4772], zoom_start=8)  # Координаты примерного центра региона

# Добавление линий для обозначения рек (примерные координаты)
shilik_coords = [(50.1296, 83.4772), (50.1300, 83.4800)]  # Примерные координаты
sharyn_coords = [(50.1100, 83.4500), (50.1150, 83.4600)]  # Примерные координаты

folium.PolyLine(shilik_coords, color="blue", weight=2.5, opacity=1).add_to(m)
folium.PolyLine(sharyn_coords, color="green", weight=2.5, opacity=1).add_to(m)

# Функция для добавления маркеров на карту
def add_drought_markers(drought_periods, coords, river_name, color):
    for start_date, end_date in drought_periods:
        folium.Marker(
            location=coords[0],
            popup=f"{river_name} Засуха с {start_date.date()} по {end_date.date()}",
            icon=folium.Icon(color=color)
        ).add_to(m)

# Добавление маркеров для периодов засухи
add_drought_markers(shilik_drought_periods, shilik_coords, "Шилик", "red")
add_drought_markers(sharyn_drought_periods, sharyn_coords, "Шарын", "purple")

# Сохранение карты в файл
m.save("135.html")