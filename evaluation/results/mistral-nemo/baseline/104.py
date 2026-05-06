import geopandas as gpd
from shapely.geometry import Point, LineString
import numpy as np
import folium

# 1. Загрузить данные о реках в формате вектора.
rivers = gpd.read_file('rivers.shp')

# 2. Выбрать реки Шыжын и Дос по их именам.
shyzyn = rivers[rivers['name'] == 'Шыжын']
dos = rivers[rivers['name'] == 'Дос']

# 3. Проверить, является ли река Шыжын притоком реки Дос.
if shyzyn.geometry.iloc[0].within(dos.geometry.iloc[0]):
    print('Река Шыжын является притоком реки Дос.')
else:
    print('Река Шыжын не является притоком реки Дос.')

# 4. Найти расстояние до их слияния, если река Шыжын является притоком.
if shyzyn.geometry.iloc[0].within(dos.geometry.iloc[0]):
    intersection = shyzyn.geometry.iloc[0].intersection(dos.geometry.iloc[0])
    distance = intersection.distance(shyzyn.geometry.iloc[0])
    print(f'Расстояние до их слияния: {distance} метров.')
else:
    print('Невозможно найти расстояние, так как река Шыжын не является притоком реки Дос.')

# 5. Визуализировать результаты на карте.
m = folium.Map(location=[shyzyn.geometry.y.mean(), shyzyn.geometry.x.mean()], zoom_start=10)
folium.GeoJson(shyzyn[['geometry']]).add_to(m)
folium.GeoJson(dos[['geometry']]).add_to(m)

if shyzyn.geometry.iloc[0].within(dos.geometry.iloc[0]):
    folium.Marker([intersection.y, intersection.x], popup='Слияние').add_to(m)

m.save("104.html")