import geopandas as gpd
import folium
from shapely.geometry import Point

# Загрузка данных о реках из OpenStreetMap (пример)
url = "https://overpass-api.de/api/interpreter?data=[out:json][timeout:425];way[highway=river](around:1000,37.6897,55.7558);node(w);out;"
response = requests.get(url)
data = response.json()

# Парсинг данных
features = data['elements']
geoms = []
for feature in features:
    if 'geometry' in feature and feature['geometry']['type'] == 'LineString':
        coords = [(coord[1], coord[0]) for coord in feature['geometry']['coordinates']]
        geoms.append(coords)

# Создание GeoDataFrame
gdf_rivers = gpd.GeoDataFrame(geometry=[LineString(geom) for geom in geoms])

# Фильтрация данных по названиям рек
target_river_names = ["Уржар", "Дос", "Каратал"]
filtered_gdf = gdf_rivers[gdf_rivers['name'].isin(target_river_names)]

# Создание карты
m = folium.Map(location=[55.7558, 37.6897], zoom_start=10)

# Добавление рек на карту
for _, row in filtered_gdf.iterrows():
    folium.PolyLine(row['geometry'].coords, color='blue', weight=2).add_to(m)

# Сохранение карты
m.save("103.html")