import pandas as pd
from folium import Map, Marker
import matplotlib.pyplot as plt

# Сбор данных о добыче золота в разных странах и регионах за XIX и XX века.
data_xix = {
    'Страна': ['Россия', 'США', 'Канада', 'Австралия'],
    'Добыча (тонн)': [100, 200, 300, 400],
    'Год': [1800, 1850, 1900, 1950]
}

data_xx = {
    'Страна': ['Россия', 'США', 'Канада', 'Австралия'],
    'Добыча (тонн)': [500, 600, 700, 800],
    'Год': [2000, 2050, 2100, 2150]
}

df_xix = pd.DataFrame(data_xix)
df_xx = pd.DataFrame(data_xx)

# Создание географической базы данных.
from geopandas import GeoDataFrame
from shapely.geometry import Point

gdf = GeoDataFrame(df_xix, geometry=[Point(long, lat) for long, lat in zip(df_xix['Добыча (тонн)'], df_xix['Год'])])

# Анализ данных для определения тенденций и закономерностей добычи золота.
import numpy as np

xix_mean = np.mean(df_xix['Добыча (тонн)'])
xx_mean = np.mean(df_xx['Добыча (тонн)'])

print(f'Средняя добыча золота в XIX веке: {xix_mean} тонн')
print(f'Средняя добыча золота в XX веке: {xx_mean} тонн')

# Визуализация результатов на карте.
m = Map(location=[40, 0], zoom_start=2)
for i in range(len(df_xix)):
    Marker(location=[df_xix['Добыча (тонн)'].iloc[i], df_xix['Год'].iloc[i]], popup=f'Добыча золота в {df_xix["Страна"].iloc[i]}').add_to(m)

m.save("274.html")