import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром на centroid basin_data
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы ровнинного участка на карте
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат фермерских хозяйств (WKT)
farmer_locations = [
    {"name": "Farm1", "geometry": wkt.loads("POINT(45.1234 78.9012)")},
    {"name": "Farm2", "geometry": wkt.loads("POINT(46.1234 79.9012)")},
    # Добавьте больше фермерских хозяйств по необходимости
]

# Визуализация фермерских хозяйств на карте
for farm in farmer_locations:
    folium.Marker([farm['geometry'].y, farm['geometry'].x], popup=farm['name']).add_to(m)

# Сохранение карты в файл
m.save("41.html")