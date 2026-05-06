import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# 1. Сбор данных о водопользовании в бассейне реки Или.
# Предполагается, что у нас есть CSV-файл с данными о водозаборах и их объемах потребления воды.
data = pd.read_csv('water_consumption.csv')

# 2. Геокодирование этих данных для привязки их к местоположению на карте.
geometry = [Point(xy) for xy in zip(data['longitude'], data['latitude'])]
gdf = gpd.GeoDataFrame(data, geometry=geometry)

# 3. Расчет объема воды, потребляемой каждым источником водопользования.
gdf['consumption'] = gdf['volume'] / gdf['duration']

# 4. Суммирование всех объемов потребления для получения общего текущего уровня потребления воды реки Или.
total_consumption = gdf['consumption'].sum()

print(f'Текущий уровень потребления воды реки Или: {total_consumption} куб. м/сут.')

# 5. Визуализация результатов на карте с использованием библиотеки `folium`.
m = folium.Map(location=[43.26, 72.58], zoom_start=8) # Координаты реки Или

for index, row in gdf.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=row['consumption']/1000,
        color='blue',
        fill=True
    ).add_to(m)

# Сохранение карты в файл "31.html"
m.save("31.html")