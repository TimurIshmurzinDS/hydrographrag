import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне в системе координат EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_data.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту с прозрачностью 20%
folium.GeoJson(data=basin_data.to_json(), name='бассейн',
                style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка наблюдений с повышенным уровнем воды
observations = [
    {"name": "Река выше Бартогайского водохранилища", "location": [43.123, 79.456]},
    {"name": "Река выше Бартогайского водохранилища", "location": [43.234, 79.567]},
    {"name": "Река выше Бартогайского водохранилища", "location": [43.345, 79.678]}
]

# Добавление наблюдений на карту
for observation in observations:
    folium.Marker(location=observation["location"], popup=observation["name"]).add_to(m)

# Сохранение карты в файл
m.save("148.html")