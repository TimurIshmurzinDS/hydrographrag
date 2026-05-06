import geopandas as gpd
import rasterio
from rasterio.mask import mask
import folium
import numpy as np
from shapely.geometry import shape

# Предположим, что у нас есть геоданные о рельефе местности и границы бассейна реки Или.
# Эти данные могут быть загружены из файлов формата GeoTIFF и Shapefile соответственно.

# Загрузка данных
elevation_raster = rasterio.open('elevation.tif')  # Файл с рельефом местности
ili_basin_shapefile = gpd.read_file('ili_basin.shp')  # Файл с границами бассейна реки Или

# Маскировка растра по границам бассейна
elevation_data, transform = mask(elevation_raster, ili_basin_shapefile.geometry, crop=True)

# Простая модель для оценки потенциала паводков (пример)
# Предположим, что высота воды пропорциональна высоте рельефа
flood_potential = elevation_data * 0.1  # Упрощенная формула

# Преобразование массива данных в GeoDataFrame для визуализации
flooding_gdf = gpd.GeoDataFrame(geometry=[shape(elevation_raster.bounds)])
flooding_gdf['flood_potential'] = flood_potential.mean()

# Создание интерактивной карты с использованием folium
m = folium.Map(location=[42.8746, 75.1950], zoom_start=10)  # Координаты примерно по центру бассейна реки Или

# Добавление слоя с данными о потенциале паводков
folium.Choropleth(
    geo_data=flooding_gdf,
    name='choropleth',
    data=flooding_gdf,
    columns=['geometry', 'flood_potential'],
    key_on='feature.geometry',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Потенциал паводков'
).add_to(m)

# Добавление слоя с границами бассейна реки Или
folium.GeoJson(ili_basin_shapefile).add_to(m)

# Сохранение карты в файл
m.save("156.html")