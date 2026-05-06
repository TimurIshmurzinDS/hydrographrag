import rasterio
from rasterio.plot import show
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium

# Загрузка DEM и гидрографических данных
dem = rasterio.open('path_to_DEM.tif')
rivers = gpd.read_file('path_to_rivers.shp')

# Определение водосбора для каждой реки
catchment_ili = ... # Используйте библиотеку GDAL/GDAL Python bindings

# Гидрологическая модель (например, HEC-HMS)
# Настройка модели с использованием исторических данных о паводках

# Расчет вероятности экстремальных событий
extreme_flood_probability = ... # Используйте HEC-HMS для расчета

# Визуализация на карте
m = folium.Map(location=[43.25, 76.9], zoom_start=8)
folium.GeoJson('path_to_rivers.shp').add_to(m)

# Добавление слоя вероятности экстремальных паводков
# ...

m.save("164.html")