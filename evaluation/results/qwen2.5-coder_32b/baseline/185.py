import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть два файла CSV: 'water_consumption.csv' и 'crop_yield.csv'
# water_consumption.csv содержит данные о водном потоке в реке Бызж (дата, объем)
# crop_yield.csv содержит данные об урожайности культур (дата, культура, участок, урожайность)

water_data = pd.read_csv('water_consumption.csv', parse_dates=['date'])
crop_data = pd.read_csv('crop_yield.csv', parse_dates=['date'])

# Шаг 2: Предварительная обработка данных
# Пример предобработки: удаление пропусков и выравнивание временных рядов

water_data.dropna(inplace=True)
crop_data.dropna(inplace=True)

# Выравниваем данные по дате
merged_data = pd.merge(water_data, crop_data, on='date')

# Шаг 3: Анализ корреляции
# Используем коэффициент Пирсона для определения корреляции

correlation_matrix = merged_data.groupby('участок').apply(lambda x: pearsonr(x['объем'], x['урожайность'])[0])
print("Коэффициенты корреляции по участкам:")
print(correlation_matrix)

# Шаг 4: Визуализация данных
# Создаем карту с отображением уровня корреляции на участках

# Предположим, что у нас есть файл 'locations.csv' с координатами участков (участок, широта, долгота)
locations = pd.read_csv('locations.csv')

# Объединяем данные о корреляции и локациях
correlation_map_data = correlation_matrix.reset_index()
correlation_map_data.rename(columns={0: 'корреляция'}, inplace=True)

merged_map_data = pd.merge(locations, correlation_map_data, on='участок')

# Создаем карту с помощью folium
m = folium.Map(location=[54.7186, 20.5111], zoom_start=9)  # Координаты примерного центра региона

for _, row in merged_map_data.iterrows():
    folium.CircleMarker(
        location=(row['широта'], row['долгота']),
        radius=10,
        color='blue',
        fill=True,
        fill_color='blue' if row['корреляция'] > 0 else 'red',
        fill_opacity=abs(row['корреляция']),
        popup=f"Участок: {row['участок']}, Корреляция: {row['корреляция']:.2f}"
    ).add_to(m)

# Сохраняем карту
m.save("185.html")