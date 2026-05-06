import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для информации)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Наблюдения уровня воды (hardcoded)
water_levels = [
    {"name": "Уровень 1", "geometry": wkt.loads("POINT(76.9534 43.2289)")},
    {"name": "Уровень 2", "geometry": wkt.loads("POINT(76.9540 43.2290)")},
    {"name": "Уровень 3", "geometry": wkt.loads("POINT(76.9545 43.2291)")},
    {"name": "Уровень 4", "geometry": wkt.loads("POINT(76.9550 43.2292)")}
]

# Добавление точек наблюдений уровня воды на карту
for level in water_levels:
    folium.Marker([level['geometry'].y, level['geometry'].x], popup=level['name'], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("15.html")