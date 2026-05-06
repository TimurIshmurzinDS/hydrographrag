import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

# Загрузка данных
data = pd.read_csv('koksu_river_data.csv', parse_dates=['date'], index_col='date')

# Проверка загруженных данных
print(data.head())

# Анализ данных
mean_water_level = data['water_level'].mean()
std_water_level = data['water_level'].std()

print(f"Среднее значение высоты воды: {mean_water_level}")
print(f"Стандартное отклонение высоты воды: {std_water_level}")

# Определение порога 50-летнего паводка
threshold_50_year_flood = mean_water_level + 2 * std_water_level

print(f"Порог 50-летнего паводка: {threshold_50_year_flood}")

# Расчет вероятности превышения порога
exceedance_probability = (data['water_level'] > threshold_50_year_flood).mean()

print(f"Вероятность превышения порога 50-летнего паводка: {exceedance_probability:.2%}")

# Визуализация данных на карте
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

for index, row in data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Date: {index.strftime('%Y-%m-%d')}, Water Level: {row['water_level']:.2f}").add_to(m)

# Сохранение карты
m.save("203.html")