import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными бассейна
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_data.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(data=basin_data.to_json(), name='бассейн').add_to(m)

# Создание списка наблюдений с координатами в WKT-формате
observations = [
    {'name': 'Улькен Алматы', 'coordinates': wkt.loads('POINT(76.923 43.233)')},
    {'name': 'Емель', 'coordinates': wkt.loads('POINT(77.123 43.333)')},
    {'name': 'Тентек', 'coordinates': wkt.loads('POINT(76.423 43.433)')}
]

# Добавление наблюдений на карту
for observation in observations:
    folium.Marker(location=observation['coordinates'].coords[0], popup=observation['name']).add_to(m)

# Сохранение карты в файл
m.save("105.html")