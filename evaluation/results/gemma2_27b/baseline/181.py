import geopandas as gpd
import rasterio
from rasterio.plot import show
import numpy as np
import folium

# Загрузка данных
river = gpd.read_file("river_shapefile.shp")
ecosystems = gpd.read_file("ecosystems_shapefile.shp")
biodiversity = gpd.read_file("biodiversity_shapefile.shp")

# Моделирование изменения уровня воды (пример)
water_level_change = 2  # Изменение уровня воды в метрах

# Оценка воздействия на экосистемы
flooded_areas = river.buffer(water_level_change)
affected_ecosystems = gpd.overlay(ecosystems, flooded_areas, how='intersection')

# Анализ биоразнообразия (пример)
species_distribution = rasterio.open("species_distribution.tif")
changed_distribution = species_distribution * affected_ecosystems.to_raster()

# Визуализация результатов
m = folium.Map(location=[river.geometry.y.mean(), river.geometry.x.mean()], zoom_start=10)
folium.GeoJson(affected_ecosystems).add_to(m)
show(changed_distribution, ax=m.axes)

# Сохранение карты
m.save("181.html")