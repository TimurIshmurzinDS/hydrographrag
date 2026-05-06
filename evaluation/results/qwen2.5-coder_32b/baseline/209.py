import geopandas as gpd
import rasterio
from rasterio.mask import mask
import numpy as np
import folium
from shapely.geometry import mapping

# Шаг 1: Сбор данных
# Предположим, что у нас есть файлы:
# - urzhar_basin.shp (геометрия бассейна реки Уржар)
# - elevation.tif (карта высот)

# Загрузка геоданных о бассейне
basin = gpd.read_file('urzhar_basin.shp')

# Загрузка карты высот
elevation = rasterio.open('elevation.tif')

# Шаг 2: Подготовка данных
# Обрезаем карту высот по границам бассейна
out_image, out_transform = mask(elevation, basin.geometry, crop=True)
elevation_data = out_image[0]

# Шаг 3: Моделирование гидрологической системы
# Для простоты моделируем наводнения на основе карты высот и предполагаемого уровня воды.
# Предположим, что уровень воды при экстремальных осадках будет выше среднего уровня на 5 метров.

mean_elevation = np.mean(elevation_data)
flood_level = mean_elevation + 5

# Создаем бинарную карту наводнений
flooding_map = elevation_data < flood_level

# Шаг 4: Анализ риска
# Преобразуем бинарную карту в геометрические объекты для визуализации
flooding_polygons = []
for geom, value in zip(basin.geometry, flooding_map):
    if value:
        flooding_polygons.append(geom)

flooding_gdf = gpd.GeoDataFrame(geometry=flooding_polygons, crs=basin.crs)

# Шаг 5: Визуализация результатов
# Создаем интерактивную карту с отображением зон риска
m = folium.Map(location=[48.6219, 73.0951], zoom_start=10)  # Координаты примерно по центру бассейна

# Добавляем границы бассейна на карту
folium.GeoJson(basin).add_to(m)

# Добавляем зоны риска наводнений
for _, row in flooding_gdf.iterrows():
    folium.GeoJson(row.geometry, style_function=lambda x: {'fillColor': 'blue', 'color': 'blue'}).add_to(m)

# Сохраняем карту в файл
m.save("209.html")