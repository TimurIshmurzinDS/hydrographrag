import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реке Турген
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.apply(lambda x: x.wkt), 
               name='Бассейн реки Турген',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка наблюдений из села Тавурген
observations = [
    {"name": "Тавурген", "coordinates": wkt.loads("POINT(75.1234 46.5678)")},
    {"name": "Тавурген", "coordinates": wkt.loads("POINT(75.2345 46.6789)")},
    {"name": "Тавурген", "coordinates": wkt.loads("POINT(75.3456 46.7890)")},
    {"name": "Тавурген", "coordinates": wkt.loads("POINT(75.4567 46.8901)")},
    {"name": "Тавурген", "coordinates": wkt.loads("POINT(75.5678 46.9012)")},
]

# Добавление наблюдений на карту
for observation in observations:
    folium.Marker(observation["coordinates"], popup=observation["name"]).add_to(m)

# Сохранение карты в файл
m.save("183.html")