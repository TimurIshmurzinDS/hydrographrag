import pandas as pd
import matplotlib.pyplot as plt
import folium

# Загружаем данные о расходе воды за последние два десятилетия в DataFrame Pandas
data = pd.read_csv('water_data.csv')

# Отфильтровываем данные, чтобы получить только те записи, которые относятся к реке Karkara River
karkara_data = data[data['river'] == 'Karkara River']

# Рассчитываем средний расход воды для каждого из последних двух десятилетий
last_decade_avg = karkara_data[karkara_data['year'] >= 2010]['flow'].mean()
prev_decade_avg = karkara_data[(karkara_data['year'] >= 2000) & (karkara_data['year'] < 2010)]['flow'].mean()

# Вычисляем разницу в расходе воды между этими двумя периодами
difference = last_decade_avg - prev_decade_avg

# Визуализируем результаты на карте с помощью библиотеки Folium
m = folium.Map(location=[51.7683, 49.2235], zoom_start=10) # Координаты реки Karkara River
folium.CircleMarker(location=[51.7683, 49.2235], radius=difference/1000, color='red', fill=True).add_to(m)
m.save("54.html")