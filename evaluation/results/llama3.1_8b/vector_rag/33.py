import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создать карту Folium с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(data=basin_data.to_json(), name='basin').add_to(m)

# Создать список точек наблюдения из контекста
observation_points = [
    {'type': 'Point', 'coordinates': [0, 0]},  # Точка наблюдения 0.2 км выше устья реки Оск
]

# Добавить точки наблюдения на карту
for point in observation_points:
    folium.Marker(location=point['coordinates'], popup='Точка наблюдения').add_to(m)

# Сохранить карту в файл
m.save("33.html")