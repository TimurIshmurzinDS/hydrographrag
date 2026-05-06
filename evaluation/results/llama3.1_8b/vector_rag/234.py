import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне в формате shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту с зеленой заливкой
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.apply(lambda x: x.wkt), 
               name='basin',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка с координатами (WKT) для реки Шарын
sharyn_river_coords = [
    {"lat": 47.1234, "lon": 86.5432},
    {"lat": 47.2345, "lon": 86.6543},
    # Добавьте остальные координаты реки Шарын в этот список
]

# Создание карты с маркерами для реки Шарын
for coord in sharyn_river_coords:
    folium.Marker([coord['lat'], coord['lon']], 
                  popup='Река Шарын').add_to(m)

# Сохранение карты в файл html
m.save("234.html")