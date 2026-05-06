import rasterio
from rasterio.plot import show
import geopandas as gpd
import folium

# Загрузка данных ЦМР
dem_path = "path/to/dem.tif"  
with rasterio.open(dem_path) as src:
    dem = src.read(1)

# Загрузка данных о уровнях воды
water_level = 5.0 # Примерный уровень воды во время паводка (в метрах)

# Создание модели inundation (упрощенная версия)
inundation_mask = dem < water_level

# Сохранение inundation mask в GeoTIFF
with rasterio.open(
    "inundation_mask.tif",
    "w",
    driver="GTiff",
    height=dem.shape[0],
    width=dem.shape[1],
    count=1,
    dtype=dem.dtype,
    crs=src.crs,
    transform=src.transform,
) as dst:
    dst.write(inundation_mask.astype(dem.dtype), 1)

# Визуализация на карте folium
m = folium.Map(location=[50.78, 16.6], zoom_start=12) # Примерные координаты реки Osek River

# Добавление inundation mask на карту
inundation_gdf = gpd.read_file("inundation_mask.tif")
folium.GeoJson(inundation_gdf, style_function=lambda feature: {'fillColor': 'blue', 'color': 'blue', 'weight': 2, 'fillOpacity': 0.5}).add_to(m)

# Сохранение карты
m.save("19.html")