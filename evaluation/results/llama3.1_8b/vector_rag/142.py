import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты Folium с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту с прозрачностью 20%
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.apply(lambda x: x.wkt), 
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка наблюдений
observations = [
    {"location": wkt.loads("POINT(54.1234 35.5678)"), "name": "Наблюдение 1"},
    {"location": wkt.loads("POINT(54.2345 35.6789)"), "name": "Наблюдение 2"},
    {"location": wkt.loads("POINT(54.3456 35.7890)"), "name": "Наблюдение 3"}
]

# Добавление наблюдений на карту
for observation in observations:
    folium.Marker(observation["location"].coords, popup=observation["name"]).add_to(m)

# Сохранение карты в файл
m.save("142.html")