import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile бассейна в CRS 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(basin_gdf.to_crs('EPSG:4326').geometry.__geo_interface__, 
               name='Бассейн реки Талгар',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка точек слияния на основе предоставленной информации
points_of_confluence = [
    {"name": "Точка слияния 1", "geometry": wkt.loads("POINT(76.9833 43.2333)")},
    {"name": "Точка слияния 2", "geometry": wkt.loads("POINT(77.0833 43.3333)")},
]

# Добавление точек слияния на карту
for point in points_of_confluence:
    folium.Marker(point['geometry'].coords[0], popup=point['name']).add_to(m)

# Сохранение карты в файл
m.save("166.html")