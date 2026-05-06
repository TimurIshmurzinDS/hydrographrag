import rasterio
from scipy.ndimage import gaussian_filter, gradient
import numpy as np
import folium

# Загрузка данных о рельефе
with rasterio.open('path/to/dem.tif') as src:
    dem = src.read(1)

# Обработка данных о рельефе
filtered_dem = gaussian_filter(dem, sigma=2)
textured_dem = gradient(filtered_dem, axis=(0, 1))

# Визуализация на карте
m = folium.Map(location=[43.25, 76.9], zoom_start=12)
folium.raster_layers.ImageOverlay(
    image=textured_dem, bounds=src.bounds, opacity=0.8
).add_to(m)

# Сохранение карты
m.save("255.html")