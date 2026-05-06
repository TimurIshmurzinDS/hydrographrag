import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с данными о бассейне
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt), 
               name='basin',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка наблюдений
observations = [
    {"time": "2023-02-20", "location": wkt.loads("POINT(48.6784 2.9535)"), "value": 100},
    {"time": "2023-02-21", "location": wkt.loads("POINT(48.6791 2.9542)"), "value": 120},
    {"time": "2023-02-22", "location": wkt.loads("POINT(48.6798 2.9550)"), "value": 110}
]

# Создание блокчейна
blockchain = []
for observation in observations:
    blockchain.append({"time": observation["time"], "location": str(observation["location"]), "value": observation["value"]})

# Сохранение карты в файл
m.save("238.html")