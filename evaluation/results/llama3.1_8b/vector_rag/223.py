import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне в формате shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка наблюдений за уровнем воды в деревне Баянколь
observations = [
    {'location': 'Баянколь', 'level': 10},
    {'location': 'Баянколь', 'level': 12},
    {'location': 'Баянколь', 'level': 11},
    {'location': 'Баянколь', 'level': 13}
]

# Добавление наблюдений на карту
for observation in observations:
    folium.Marker(location=[observation['location'], 0], popup=f'Уровень воды: {observation["level"]}').add_to(m)

# Сохранение карты в файл
m.save("223.html")