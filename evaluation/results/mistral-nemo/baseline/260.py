import geopandas as gpd
from shapely.geometry import Point
import folium

# Шаг 1: Сбор данных о местоположении реки Караой
river_name = "Караой"
geometry = Point(74.56, 42.87) # Примерные координаты реки Караой
gdf = gpd.GeoDataFrame({'geometry': [geometry]}, crs="EPSG:4326")

# Шаг 2: Визуализация местоположения реки на карте
m = folium.Map(location=[42.87, 74.56], zoom_start=10)
folium.GeoJson(gdf.to_json(), style_function=lambda x: {'fillColor': 'blue'}).add_to(m)

# Шаг 3: Добавление метки на карту
folium.Marker([42.87, 74.56], popup=river_name).add_to(m)

# Сохранение карты в HTML-файл
m.save("260.html")