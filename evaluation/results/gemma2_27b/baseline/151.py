import rasterio
from rasterio.plot import show
import numpy as np
import matplotlib.pyplot as plt
import folium

# Загрузка DEM
dem = rasterio.open('path_to_DEM.tif')
elevation = dem.read(1)

# Определение зон водосбора (пример, нужно адаптировать к конкретным данным)
watershed_bayankol = np.where(elevation < 1000, 1, 0)
watershed_ili = np.where(elevation < 1200, 1, 0)

# Гидравлическое моделирование (пример, нужно адаптировать к конкреным данным)
# ...

# Визуализация на карте
m = folium.Map(location=[43.5, 78], zoom_start=8)

# Добавление DEM
show(elevation, cmap='terrain', ax=plt.gca())

# Добавление зон риска (пример)
folium.GeoJson(data=watershed_bayankol, name="Bayankol River Watershed").add_to(m)
folium.GeoJson(data=watershed_ili, name="Ili River Watershed").add_to(m)

# Сохранение карты
m.save("151.html")