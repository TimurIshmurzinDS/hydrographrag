import geopandas as gpd
from rasterio.plot import show
import rasterio
import folium

# Загрузка данных о бассейне реки Или
basin = gpd.read_file("ili_basin.shp")

# Загрузка данных о землепользовании
landuse = rasterio.open("landuse.tif")

# Классификация зон землепользования
# ... (код для классификации зон землепользования)

# Расчет объемов воды для каждого типа орошения
# ... (код для расчета объемов воды)

# Создание карты с folium
m = folium.Map(location=[43, 80], zoom_start=6)

# Добавление границ бассейна на карту
folium.GeoJson(basin).add_to(m)

# Добавление зон орошения на карту
# ... (код для добавления зон орошения на карту с цветовой градацией по объему воды)

m.save("39.html")