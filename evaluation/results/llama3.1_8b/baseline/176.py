import geopandas as gpd
from shapely.geometry import Point
from folium import Map, Marker
import pandas as pd

# Загрузим данные о геометрии ручьев и рек
gdf_river = gpd.read_file('river.shp')
gdf_terisbutak = gpd.read_file('terisbutak.shp')

# Рассчитаем расстояние от каждого участка русла ручья Терисбутак до ближайшей точки на реке Талгар
def calculate_distance(gdf1, gdf2):
    distances = []
    for index, row in gdf1.iterrows():
        min_dist = float('inf')
        for index2, row2 in gdf2.iterrows():
            dist = row.geometry.distance(row2.geometry)
            if dist < min_dist:
                min_dist = dist
        distances.append(min_dist)
    return distances

distances = calculate_distance(gdf_terisbutak, gdf_river)

# Сгруппируем расстояния по квантилям (например, 10%, 25%, 50% и т.д.)
quantiles = pd.qcut(distances, q=[0, 0.1, 0.25, 0.5, 0.75, 0.9, 1])

# Визуализируем результаты на карте
m = Map(location=[43.2, 76.7], zoom_start=10)
for index, row in gdf_terisbutak.iterrows():
    marker = Marker(row.geometry.centroid, popup=str(quantiles.iloc[index]))
    m.add_child(marker)

# Сохраняем карту в файл
m.save("176.html")