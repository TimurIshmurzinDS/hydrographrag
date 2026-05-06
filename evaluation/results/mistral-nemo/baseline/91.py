import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# 1. Прочитать данные о реках из Shapefile
rivers = gpd.read_file("rivers.shp")

# 2. Фильтровать данные, чтобы найти только те реки, которые являются притоками реки Уржар
urjar_rivers = rivers[rivers['name'] == 'Уржар']
pritochnye_reki = rivers[rivers.intersects(urjar_rivers.unary_union)]

# 3. Сохранить координаты найденных притоков в список кортежей (имя реки, долгота, широта)
coordinates = [(row['name'], row.geometry.x, row.geometry.y) for _, row in pritochnye_reki.iterrows()]

# 4. Визуализировать результаты на карте с помощью библиотеки Folium и сохранить файл как "91.html"
m = folium.Map(location=[pritochnye_reki.geometry.y.mean(), pritochnye_reki.geometry.x.mean()], zoom_start=8)

for name, lon, lat in coordinates:
    folium.Marker([lat, lon], popup=name).add_to(m)

m.save("91.html")