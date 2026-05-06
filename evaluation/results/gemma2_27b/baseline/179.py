import rasterio
from rasterio.plot import show
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import folium

# Загрузка данных
river_network = gpd.read_file("path/to/river_network.shp")
dem = rasterio.open("path/to/dem.tif")

# Предобработка речной сети
river_network = river_network.dissolve()

# Гидравлический анализ (D8 flow direction)
flow_direction = np.gradient(dem, axis=0)

# Определение зоны затопления
flood_zone = np.where(flow_direction > 0, 1, 0)

# Визуализация на карте
m = folium.Map(location=[river_network.geometry.y.mean(), river_network.geometry.x.mean()], zoom_start=12)
folium.GeoJson(river_network).add_to(m)
folium.raster_layers.ImageOverlay(flood_zone, bounds=river_network.total_bounds).add_to(m)

# Сохранение карты
m.save("179.html")