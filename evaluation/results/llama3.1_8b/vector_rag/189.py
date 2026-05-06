import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка наблюдений
observations = [
    {'id': 1, 'location': wkt.loads('POINT(48.1234 86.5432)')},
    {'id': 2, 'location': wkt.loads('POINT(48.1245 86.5443)')},
    {'id': 3, 'location': wkt.loads('POINT(48.1256 86.5454)')},
    {'id': 4, 'location': wkt.loads('POINT(48.1267 86.5465)')},
    {'id': 5, 'location': wkt.loads('POINT(48.1278 86.5476)')}
]

# Добавление наблюдений на карту
for observation in observations:
    folium.Marker(observation['location'], popup=f'Наблюдение {observation["id"]}').add_to(m)

# Сохранение карты
m.save("189.html")