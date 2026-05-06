import pandas as pd
from folium import Map, Marker, CircleMarker
import geopandas as gpd
from shapely.geometry import Point

# Загрузка данных о климате и гидрологии для рек Aksu и Temirlik
data_aksu = pd.read_csv('aksu_data.csv')
data_temirlik = pd.read_csv('temirlik_data.csv')

# Объединение данных в одну таблицу
data_combined = pd.concat([data_aksu, data_temirlik])

# Создание геообработки для обоих рек
gdf_aksu = gpd.GeoDataFrame(data_aksu, geometry=gpd.points_from_xy(data_aksu['long'], data_aksu['lat']))
gdf_temirlik = gpd.GeoDataFrame(data_temirlik, geometry=gpd.points_from_xy(data_temirlik['long'], data_temirlik['lat']))

# Определение площади водосбора и скорости стока для обоих рек
gdf_aksu['area'] = gdf_aksu.geometry.area
gdf_aksu['speed'] = gdf_aksu.geometry.length / (data_aksu['discharge'] ** 2)

gdf_temirlik['area'] = gdf_temirlik.geometry.area
gdf_temirlik['speed'] = gdf_temirlik.geometry.length / (data_temirlik['discharge'] ** 2)

# Создание модели риска засухи на основе анализа данных и геообработки
risk_model_aksu = data_aksu['evaporation'] * data_aksu['area'] + data_aksu['speed']
risk_model_temirlik = data_temirlik['evaporation'] * data_temirlik['area'] + data_temirlik['speed']

# Визуализация результатов на карте с помощью библиотеки Folium
m = Map(location=[40.0, 70.0], zoom_start=6)
Marker([data_aksu['lat'].mean(), data_aksu['long'].mean()], popup='Река Аксу').add_to(m)
CircleMarker([data_aksu['lat'].mean(), data_aksu['long'].mean()], radius=data_aksu['area'].mean()).add_to(m)

m = Map(location=[40.0, 70.0], zoom_start=6)
Marker([data_temirlik['lat'].mean(), data_temirlik['long'].mean()], popup='Река Темирлик').add_to(m)
CircleMarker([data_temirlik['lat'].mean(), data_temirlik['long'].mean()], radius=data_temirlik['area'].mean()).add_to(m)

# Сохранение карты в файл
m.save("111.html")