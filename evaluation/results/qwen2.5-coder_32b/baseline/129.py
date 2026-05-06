import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

# Предположим, что у нас есть данные в формате CSV с колонками: 'date', 'discharge', 'river'
# Загрузка данных для Kurty River и Tekes River
kurty_data = pd.read_csv('kurty_river_discharge.csv', parse_dates=['date'])
tekes_data = pd.read_csv('tekes_river_discharge.csv', parse_dates=['date'])

# Очистка данных от пропусков
kurty_data.dropna(inplace=True)
tekes_data.dropna(inplace=True)

# Функция для определения периода весеннего половодья (март-апрель)
def is_spring_flood(date):
    return date.month in [3, 4]

# Выделение данных за периоды весеннего половодья
kurty_spring = kurty_data[kurty_data['date'].apply(is_spring_flood)]
tekes_spring = tekas_data[tekas_data['date'].apply(is_spring_flood)]

# Группировка данных по годам и расчет среднего расхода воды за весеннее половодье
kurty_spring_avg = kurty_spring.groupby(kurty_spring['date'].dt.year)['discharge'].mean().reset_index()
tekes_spring_avg = tekas_spring.groupby(tekas_spring['date'].dt.year)['discharge'].mean().reset_index()

# Построение графиков для сравнения среднего расхода воды
plt.figure(figsize=(12, 6))
plt.plot(kurty_spring_avg['year'], kurty_spring_avg['discharge'], label='Kurty River', marker='o')
plt.plot(tekes_spring_avg['year'], tekas_spring_avg['discharge'], label='Tekes River', marker='o')
plt.title('Средний расход воды в реках Kurty и Tekes за период весеннего половодья (2018-2023)')
plt.xlabel('Год')
plt.ylabel('Расход воды, м³/с')
plt.legend()
plt.grid(True)
plt.show()

# Создание карты с использованием folium
m = folium.Map(location=[42.5, 79], zoom_start=8)

# Координаты рек (примерные значения)
kurty_coords = [43.0167, 79.25]
tekes_coords = [42.5, 80]

folium.Marker(kurty_coords, popup='Kurty River', icon=folium.Icon(color='blue')).add_to(m)
folium.Marker(tekes_coords, popup='Tekes River', icon=folium.Icon(color='green')).add_to(m)

# Сохранение карты в файл
m.save("129.html")