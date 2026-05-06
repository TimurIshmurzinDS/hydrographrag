import pandas as pd
import numpy as np
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть CSV-файл с данными о расходах воды
data = pd.read_csv('water_consumption.csv')

# Пример структуры данных:
# date, location, water_usage (куб. м)
# 2023-01-01, Кумбель_АПК1, 5000
# 2023-01-01, Кумбель_АПК2, 7000

# Шаг 2: Обработка данных
data['date'] = pd.to_datetime(data['date'])
data.dropna(inplace=True)

# Шаг 3: Анализ данных
# Вычисление среднего ежемесячного расхода воды для каждого АПК
monthly_usage = data.groupby([data['date'].dt.year, data['date'].dt.month, 'location'])['water_usage'].sum().reset_index()
average_monthly_usage = monthly_usage.groupby('location')['water_usage'].mean().reset_index()

# Шаг 4: Визуализация данных
# Создание карты с использованием folium
m = folium.Map(location=[51.678, 39.204], zoom_start=10)  # Координаты примерного расположения реки Кумбель

# Добавление маркеров на карту для каждого АПК с информацией о среднем ежемесячном расходе воды
for index, row in average_monthly_usage.iterrows():
    location_name = row['location']
    avg_water_usage = row['water_usage']
    
    # Предположим, что у нас есть словарь с координатами каждого АПК
    coordinates = {
        'Кумбель_АПК1': [51.680, 39.206],
        'Кумбель_АПК2': [51.675, 39.210]
    }
    
    if location_name in coordinates:
        folium.Marker(
            location=coordinates[location_name],
            popup=f"APK: {location_name}<br>Средний ежемесячный расход воды: {avg_water_usage} куб. м",
            icon=folium.Icon(color='blue')
        ).add_to(m)

# Шаг 5: Сохранение результата
m.save("37.html")