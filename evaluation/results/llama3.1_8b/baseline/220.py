import pandas as pd
import geopandas as gpd
from folium import Map, Marker

# Сбор и очистка данных
data = pd.read_csv('датчики_батарейки_ривер.csv')
data.dropna(inplace=True)

# Геопозиционирование данных
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['долгота'], data['широта']))

# Создание модели
model = {
    'скорость': 100,
    'направление': 45,
    'координаты': (data['долгота'].mean(), data['широта'].mean())
}

# Визуализация на карте
m = Map(location=[model['координаты'][1], model['координаты'][0]], zoom_start=10)
Marker([model['координаты'][1], model['координаты'][0]]).add_to(m)

# Добавление маркеров для датчиков
for index, row in data.iterrows():
    Marker([row['широта'], row['долгота']]).add_to(m)

m.save("220.html")