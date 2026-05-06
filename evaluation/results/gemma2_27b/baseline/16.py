import geopandas as gpd
from rasterio import open as rio_open
import folium
import numpy as np

# Загрузка данных
dem = rio_open("path/to/dem.tif")  # Заменить на путь к файлу ЦМР
river_data = gpd.read_file("path/to/river_data.shp") # Заменить на путь к файлу с данными о реке

# Гидрологическое моделирование (используя библиотеку, например, HEC-HMS)
# ...

# Определение зон затопления
flood_zones = gpd.GeoDataFrame(...)  # Результаты гидрологического моделирования

# Визуализация на карте
m = folium.Map(location=[43.25, 76.9], zoom_start=12)
folium.GeoJson(flood_zones).add_to(m)
river_data.plot(ax=m.get_axes(), color='blue')

# Сохранение карты
m.save("16.html")