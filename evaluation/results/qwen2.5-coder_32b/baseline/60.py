import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть два CSV файла: 'precipitation_karkara.csv' и 'water_level_karkara.csv'
# Каждый файл содержит столбцы: 'date', 'value'

# Загрузка данных о осадках
precipitation_data = pd.read_csv('precipitation_karkara.csv', parse_dates=['date'])
precipitation_data.set_index('date', inplace=True)

# Загрузка данных об уровне воды
water_level_data = pd.read_csv('water_level_karkara.csv', parse_dates=['date'])
water_level_data.set_index('date', inplace=True)

# Шаг 2: Обработка данных
# Приведение временных рядов к одному диапазону дат и заполнение пропусков
common_dates = precipitation_data.index.intersection(water_level_data.index)
precipitation_data = precipitation_data.loc[common_dates].resample('D').mean().fillna(method='ffill')
water_level_data = water_level_data.loc[common_dates].resample('D').mean().fillna(method='ffill')

# Шаг 3: Анализ временных рядов
# Вычисление корреляции между осадками и уровнем воды
correlation, _ = pearsonr(precipitation_data['value'], water_level_data['value'])
print(f'Корреляция между осадками и уровнем воды: {correlation}')

# Шаг 4: Визуализация данных
plt.figure(figsize=(12, 6))
plt.plot(precipitation_data.index, precipitation_data['value'], label='Осадки', color='blue')
plt.plot(water_level_data.index, water_level_data['value'], label='Уровень воды', color='green')
plt.title('Сравнение осадков и уровня воды в реке Karkara River (2018-2023)')
plt.xlabel('Дата')
plt.ylabel('Значение')
plt.legend()
plt.grid(True)
plt.show()

# Шаг 5: Геоспатиальная визуализация
# Создание карты с помощью folium
m = folium.Map(location=[41.68, 70.23], zoom_start=10)  # Координаты примерного расположения реки Karkara

# Добавление маркера на карте (пример)
folium.Marker(
    location=[41.68, 70.23],
    popup='Karkara River',
    icon=folium.Icon(color='blue')
).add_to(m)

# Сохранение карты в HTML файл
m.save("60.html")