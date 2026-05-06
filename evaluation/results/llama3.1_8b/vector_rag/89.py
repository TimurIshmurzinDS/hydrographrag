import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне в формате shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту с прозрачностью 20%
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.exterior)).add_to(m)

# Создание списка наблюдений за уровнем воды на реке Prokhodnoy River
observations = [
    {'location': wkt.loads('POINT(55.123 37.456)'), 'value': 10},
    {'location': wkt.loads('POINT(55.124 37.457)'), 'value': 12},
    {'location': wkt.loads('POINT(55.125 37.458)'), 'value': 15}
]

# Добавление наблюдений на карту
for observation in observations:
    folium.Marker(location=[observation['location'].y, observation['location'].x], popup=f'Уровень воды: {observation["value"]}').add_to(m)

# Создание списка данных о расходе на реке Baskan River
discharge_data = [
    {'location': wkt.loads('POINT(55.123 37.456)'), 'value': 100},
    {'location': wkt.loads('POINT(55.124 37.457)'), 'value': 120},
    {'location': wkt.loads('POINT(55.125 37.458)'), 'value': 150}
]

# Добавление данных о расходе на карту
for discharge in discharge_data:
    folium.Marker(location=[discharge['location'].y, discharge['location'].x], popup=f'Расход: {discharge["value"]}').add_to(m)

# Сохранение карты в файл html
m.save("89.html")