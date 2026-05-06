import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import numpy as np
import folium

# 1. Получение данных о рельефе местности и положении рек.
river_data = {
    'Byzhy_River': gpd.read_file('byzhy_river.shp'),
    'Lepsy_River': gpd.read_file('lepsy_river.shp')
}

# 2. Определение точек доступа к воде вдоль реки
access_points = {}
for river, data in river_data.items():
    access_points[river] = data[data['type'] == 'access_point'].copy()

# 3. Расчет расстояний от этих точек до ближайших животноводческих ферм.
farms = gpd.read_file('farms.shp')
distances = {}
for river, points in access_points.items():
    distances[river] = []
    for _, point in points.iterrows():
        geometry = [Point(f['geometry'].x, f['geometry'].y) for _, f in farms.iterrows()]
        dist = gpd.sjoin_nearest(points, farms, how='nearest', op='distance')
        distances[river].append(dist.iloc[0]['distance'])

# 4. Вычисление среднего расстояния для каждой реки и сравнение значений.
avg_distances = {river: np.mean(dists) for river, dists in distances.items()}
print(f"Среднее расстояние до водных ресурсов в реке Byzhy River: {avg_distances['Byzhy_River']:.2f} км")
print(f"Среднее расстояние до водных ресурсов в реке Lepsy River: {avg_distances['Lepsy_River']:.2f} км")

# Визуализация на карте
m = folium.Map(location=[53.7098, 27.9517], zoom_start=8)

for river, points in access_points.items():
    for _, point in points.iterrows():
        folium.Marker([point['geometry'].y, point['geometry'].x], popup=river).add_to(m)

m.save("109.html")