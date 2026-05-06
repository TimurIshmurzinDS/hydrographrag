import pandas as pd
import numpy as np
import folium

# Шаг 1: Сбор данных
# Предположим, что данные о расходе воды находятся в CSV файле 'water_flow_data.csv'
data = pd.read_csv('water_flow_data.csv')

# Пример структуры данных:
# station_id, latitude, longitude, date, water_flow

# Шаг 2: Обработка данных
# Удаление пропусков и аномалий (значения расхода воды меньше 0)
data = data.dropna()
data = data[data['water_flow'] >= 0]

# Преобразование даты в формат datetime
data['date'] = pd.to_datetime(data['date'])

# Шаг 3: Анализ данных
# Вычисление среднего и стандартного отклонения расхода воды для каждого поста
station_stats = data.groupby('station_id')['water_flow'].agg(['mean', 'std']).reset_index()

# Определение порогового значения для наводнения (например, 2 сигмы выше среднего)
station_stats['flood_threshold'] = station_stats['mean'] + 2 * station_stats['std']

# Шаг 4: Моделирование вероятности наводнения
# Определение дней с превышением порогового значения для каждого поста
data = pd.merge(data, station_stats[['station_id', 'flood_threshold']], on='station_id')
data['is_flood'] = data['water_flow'] > data['flood_threshold']

# Шаг 5: Визуализация результатов
# Создание интерактивной карты с помощью folium
m = folium.Map(location=[42.8746, 74.5910], zoom_start=10)  # Координаты примерного центра реки Темирлик

# Добавление маркеров на карту для каждого поста с цветовой индикацией вероятности наводнения
for idx, row in data.iterrows():
    if row['is_flood']:
        color = 'red'  # Красный цвет - вероятность наводнения
    else:
        color = 'blue'  # Синий цвет - нет вероятности наводнения
    
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        popup=f"Station ID: {row['station_id']}\nDate: {row['date'].strftime('%Y-%m-%d')}\nWater Flow: {row['water_flow']} m³/s\nFlood Threshold: {row['flood_threshold']} m³/s",
        color=color,
        fill=True,
        fill_color=color
    ).add_to(m)

# Сохранение карты в HTML файл
m.save("78.html")