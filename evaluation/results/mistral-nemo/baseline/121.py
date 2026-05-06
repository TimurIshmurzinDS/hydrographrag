import pandas as pd
import numpy as np
from folium import Map, Marker, GeoJson

# Загрузка данных о расходе воды для реки Bayankol River
bayankol_data = pd.read_csv('bayankol_water_discharge.csv')

# Загрузка данных о расходе воды для реки Shilik River
shilik_data = pd.read_csv('shilik_water_discharge.csv')

# Вычисление среднего расхода воды за последние 10 лет для реки Bayankol River
bayankol_avg = bayankol_data['discharge'].rolling(window=365*10).mean().iloc[-1]

# Вычисление среднего расхода воды за последние 10 лет для реки Shilik River
shilik_avg = shilik_data['discharge'].rolling(window=365*10).mean().iloc[-1]

print(f'Средний расход воды в реке Bayankol River за последние 10 лет: {bayankol_avg}')
print(f'Средний расход воды в реке Shilik River за последние 10 лет: {shilik_avg}')

# Создание карты с помощью библиотеки folium
m = Map(location=[43.25, 76.9], zoom_start=8)

# Добавление меток для рек Bayankol и Shilik на карту
Marker([bayankol_data['latitude'].iloc[0], bayankol_data['longitude'].iloc[0]]).add_to(m)
Marker([shilik_data['latitude'].iloc[0], shilik_data['longitude'].iloc[0]]).add_to(m)

# Добавление геоданных рек на карту
geojson_bayankol = GeoJson(bayankol_data[['latitude', 'longitude']]).add_to(m)
geojson_shilik = GeoJson(shilik_data[['latitude', 'longitude']]).add_to(m)

# Сохранение карты в файл HTML
m.save("121.html")