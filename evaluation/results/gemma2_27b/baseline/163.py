import rasterio
from rasterio.plot import show
import numpy as np
import matplotlib.pyplot as plt
import folium

# Загрузка DEM
dem = rasterio.open('path_to_DEM.tif')
elevation = dem.read(1)

# Гидравлическая модель (упрощенная версия)
def water_level(precipitation, elevation):
    return elevation + 0.1 * precipitation

# Расчет уровня воды при различных условиях
precipitation = np.arange(0, 100, 1)
water_levels = water_level(precipitation, elevation)

# Создание карты Folium
m = folium.Map(location=[43.5, 78], zoom_start=10)

# Визуализация уровня воды на карте
for i in range(len(water_levels)):
    folium.GeoJson(data='path_to_river_shapefile.geojson', style_function=lambda feature: {
        'color': 'blue',
        'weight': 2,
        'fillOpacity': 0.5 * (i / len(water_levels)),
    }).add_to(m)

# Сохранение карты
m.save('163.html')