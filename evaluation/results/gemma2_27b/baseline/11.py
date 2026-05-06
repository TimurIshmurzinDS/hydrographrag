import geopandas as gpd
from rasterio.plot import show
import rasterio
from folium import Map, GeoJson

# Загрузка данных
river_line = gpd.read_file("koktal_river.shp")  # Замените на путь к файлу с линией русла
dem = rasterio.open("koktal_dem.tif") # Замените на путь к файлу ЦМР

# Определение текущего уровня воды (в метрах)
water_level = 10.5  # Замените на актуальный уровень воды

# Пересечение линии русла с ЦМР
intersection = gpd.overlay(river_line, dem.read(1), how='intersection')

# Расчет глубины
intersection['depth'] = water_level - intersection['band_1']

# Визуализация на карте
m = Map(location=[43.05, 78.6], zoom_start=12)  
GeoJson(intersection[['geometry', 'depth']]).add_to(m)
m.save("11.html")