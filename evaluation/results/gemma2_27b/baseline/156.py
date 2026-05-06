import rasterio
from rasterio.plot import show
import numpy as np
import matplotlib.pyplot as plt
import folium

# Загрузка DEM
dem = rasterio.open('path_to_DEM.tif')
elevation = dem.read(1)

# Определение водосборного бассейна (используя библиотеку, например, HydroFlow)
# ...

# Гидрологическая модель (например, HEC-HMS)
# ...

# Расчет уровней воды и зон затопления

# Визуализация в folium
m = folium.Map(location=[43.25, 78.0], zoom_start=8)
# Добавление DEM на карту
show(elevation, ax=plt.gca())
# Добавление зон риска паводков на карту

m.save("156.html")