import folium
import pyproj
from rasterio.plot import show
from rasterio.warp import reproject, Resampling
import numpy as np
import matplotlib.pyplot as plt

# 1. Определение координат реки Аксу (примерные):
lat_start = 40.5
lon_start = 72.5
lat_end = 40.0
lon_end = 73.0

# 2. Проекция на Марс:
mars_proj = pyproj.Proj(init='epsg:499001') # Mars 2000 IAU System

start_mars = pyproj.transform(pyproj.Proj(init='epsg:4326'), mars_proj, lon_start, lat_start)
end_mars = pyproj.transform(pyproj.Proj(init='epsg:4326'), mars_proj, lon_end, lat_end)

# 3. Загрузка данных о рельефе (пример):
with rasterio.open('path/to/mars_elevation.tif') as src:
    out_image, out_transform = reproject(src=src, dst_crs=mars_proj, resampling=Resampling.nearest)

# 4. Анализ рельефа (пример):
elevation_data = np.array(out_image)
suitable_locations = elevation_data[np.where((elevation_data > -1000) & (elevation_data < 1000))] #Пример: высота от -1000 до 1000 м

# 5. Визуализация на карте:
m = folium.Map(location=[lat_start, lon_start], zoom_start=4)
folium.Marker(location=[lat_start, lon_start], popup='Начало реки Аксу').add_to(m)
folium.Marker(location=[lat_end, lon_end], popup='Конец реки Аксу').add_to(m)

# Добавление точек подходящих мест (пример):
for i in range(len(suitable_locations)):
    x, y = np.where(elevation_data == suitable_locations[i])
    folium.Marker(location=[y, x], popup='Подходящее место').add_to(m)

m.save("248.html")