import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Шаг 1: Соберите данные о температуре и влажности воздуха от датчиков Kishi вдоль реки Алматы.
data = pd.read_csv('kishi_almaty_river_data.csv')

# Шаг 2: Определите оптимальные диапазоны температуры и влажности для выращивания кактусов.
temp_min, temp_max = 20, 30
humidity_min, humidity_max = 40, 60

# Шаг 3: Создайте геообласть, где эти оптимальные условия соблюдаются на основе данных датчиков.
geometry = [Point(lon, lat) for lon, lat in zip(data['longitude'], data['latitude'])]
gdf = gpd.GeoDataFrame(data, geometry=geometry)
optimal_conditions = (gdf['temperature'] >= temp_min) & (gdf['temperature'] <= temp_max) & \
                      (gdf['humidity'] >= humidity_min) & (gdf['humidity'] <= humidity_max)

# Шаг 4: Визуализируйте эту область на карте с использованием библиотек Folium и GeoPandas.
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)
folium.GeoJson(gdf[optimal_conditions].to_json(), style_function=lambda x, y, z: {'fillColor': 'green'}).add_to(m)

# Сохраните карту как "217.html"
m.save("217.html")