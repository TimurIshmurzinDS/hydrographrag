import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile в CRS 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создать карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(data=basin_gdf.unary_union.__geo_interface__, name='basin').add_to(m)

# Создать список словарей для точек наблюдения
points = [
    {'name': 'Пункт наблюдения 0,2 км выше устья реки Оск', 'geometry': wkt.loads('POINT(74.1234 56.7890)')},
    {'name': 'Пункт наблюдения 0,2 км выше устья реки Оск', 'geometry': wkt.loads('POINT(75.4567 57.8901)')}
]

# Добавить точки на карту
for point in points:
    folium.Marker(location=point['geometry'].coords[0], popup=point['name']).add_to(m)

# Сгенерировать случайные числа на основе извилистости русла реки Шилик
import random

def calculate_meandering(river_length, river_width):
    return random.uniform(1.0, 5.0) * (river_length / river_width)

shilik_river_length = 100.0  # км
shilik_river_width = 10.0  # км

meandering_value = calculate_meandering(shilik_river_length, shilik_river_width)
print(f"Извилистость русла реки Шилик: {meandering_value:.2f}")

# Сохранить карту в файл
m.save("254.html")