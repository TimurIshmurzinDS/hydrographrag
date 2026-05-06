import pandas as pd
import matplotlib.pyplot as plt
from folium import Map, Marker

# Загрузка данных о уровнях воды
water_levels = pd.read_csv('water_levels.csv')

# Анализ данных для определения периода последнего весеннего паводка
pavodok_period = water_levels.loc[(water_levels['date'] > '2020-03-01') & (water_levels['date'] < '2020-06-30')]

# Вычисление максимального уровня воды во время периода последнего весеннего паводка
max_water_level = pavodok_period['level'].max()

print(f'Максимальный уровень воды, достигнутый во время последнего весеннего паводка на реке Оск: {max_water_level} м')

# Визуализация результатов на карте с помощью библиотеки folium
m = Map(location=[55.0, 32.0], zoom_start=10)
Marker(location=[55.0, 32.0], popup=f'Максимальный уровень воды: {max_water_level} м').add_to(m)

# Сохранение карты в файл
m.save("19.html")