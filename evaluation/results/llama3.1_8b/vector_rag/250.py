import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с топографической сетью притоков реки Тентек
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине площади водосбора
m = folium.Map(location=[basin_gdf.centroid.y, basin_gdf.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление топографической сети притоков реки Тентек на карту
folium.GeoJson(data=basin_gdf.to_json(), name='basin').add_to(m)

# Создание списка наблюдательных точек (орбиты спутника)
observation_points = [
    {'name': 'Орбита 1', 'location': [0.2, 0.2], 'description': 'Наблюдательная точка 1'},
    {'name': 'Орбита 2', 'location': [0.3, 0.3], 'description': 'Наблюдательная точка 2'},
    {'name': 'Орбита 3', 'location': [0.4, 0.4], 'description': 'Наблюдательная точка 3'},
    {'name': 'Орбита 4', 'location': [0.5, 0.5], 'description': 'Наблюдательная точка 4'}
]

# Добавление наблюдательных точек на карту
for point in observation_points:
    folium.Marker(location=point['location'], popup=f"{point['name']}: {point['description']}").add_to(m)

# Сохранение карты в файл
m.save("250.html")