import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Аксу
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.apply(lambda x: x.wkt),
               name='Бассейн реки Аксу',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка наблюдений
observations = [
    {"location": "1.7 км выше устья реки Киш Оск", "value": 10},
    {"location": "1.7 км выше устья реки Киш Оск", "value": 15}
]

# Добавление наблюдений на карту
for observation in observations:
    folium.Marker(location=[observation["location"]], popup=f"Уровень воды: {observation['value']}").add_to(m)

# Сохранение карты в файл
m.save("206.html")