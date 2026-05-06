import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# 1. Создание географического слоя реки Или и определение ее бассейна.
river_gdf = gpd.read_file("il_river.shp") # Замените на путь к вашему файлу shapefile реки Или
basin_gdf = river_gdf.dissolve(by='name', aggfunc='sum') # Получение бассейна реки

# 2. Получение данных о потреблении воды для полива в этом районе.
water_use_gdf = gpd.read_file("water_use.shp") # Замените на путь к вашему файлу shapefile данных о потреблении воды
merged_gdf = pd.merge(basin_gdf, water_use_gdf, how='inner', left_on='name', right_on='river_name') # Объединение геоданных по имени реки

# 3. Вычисление объема воды, используемой для полива в бассейне реки Или.
total_water_use = merged_gdf['water_volume'].sum()

# Визуализация на карте
m = folium.Map(location=[merged_gdf.geometry.y.mean(), merged_gdf.geometry.x.mean()], zoom_start=8)
folium.GeoJson(basin_gdf, name='River Basin').add_to(m)
folium.LayerControl().add_to(m)

# Сохранение карты
m.save("39.html")