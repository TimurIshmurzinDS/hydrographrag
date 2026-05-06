import pandas as pd
from folium import Map, Marker
from folium.plugins import HeatMap

# Загрузка исторических данных о паводках
historical_data = pd.read_csv('исторические_данные.csv')

# Загрузка текущих показателей
current_data = pd.read_csv('текущие_показатели.csv')

# Сравнение исторических и текущих данных
extreme_years = historical_data.merge(current_data, on='год')
extreme_years = extreme_years[extreme_years['паводок'] > 10]

# Геоспациальное моделирование
from geopy.distance import geodesic

def calculate_distance(row):
    river_point = (row['широта'], row['долгота'])
    return geodesic((river_point, (0, 0))).miles

extreme_years['расстояние'] = extreme_years.apply(calculate_distance, axis=1)

# Визуализация на карте
m = Map(location=[55.1234, 37.5678], zoom_start=10)
HeatMap(data=extreme_years[['широта', 'долгота']].values, radius=5).add_to(m)

for index, row in extreme_years.iterrows():
    Marker([row['широта'], row['долгота']], popup=f'Год: {row["год"]}, Паводок: {row["паводок"]}').add_to(m)

m.save("200.html")