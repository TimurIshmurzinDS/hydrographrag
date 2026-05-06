import rasterio
from rasterio.plot import show
import numpy as np
import matplotlib.pyplot as plt
import folium

# Загрузка DEM
dem = rasterio.open('path_to_dem.tif')
dem_data = dem.read(1)

# Определение зоны водосбора (пример, нужно заменить на реальную функцию)
watershed_boundary = np.where(dem_data < 1000, True, False)

# Гидравлическое моделирование (пример, нужно заменить на реальную модель)
def flood_model(watershed_boundary):
    return np.where(watershed_boundary, 1, 0)

flood_potential = flood_model(watershed_boundary)

# Визуализация
m = folium.Map(location=[43.25, 78.5], zoom_start=10)
folium.rasterio.show_raster(dem, bounds=dem.bounds, name='DEM', overlay=True, colormap='viridis')

# Добавление зоны затопления на карту
flood_data = np.where(flood_potential == 1, 'red', 'transparent')
folium.GeoJson(flood_data, style_function=lambda feature: {'fillColor': feature['properties']['color'], 'fillOpacity': 0.5}).add_to(m)

# Сохранение карты
m.save("161.html")