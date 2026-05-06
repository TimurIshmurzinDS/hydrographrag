import geopandas as gpd
import rasterio
from rasterio.mask import mask
import numpy as np
import folium
from shapely.geometry import shape

# Шаг 1: Сбор данных
# Предположим, что у нас есть файлы DEM (Digital Elevation Model) и географические данные о реке.
dem_path = 'path_to_dem.tif'
river_shapefile_path = 'path_to_river.shp'

# Чтение данных
dem_dataset = rasterio.open(dem_path)
river_gdf = gpd.read_file(river_shapefile_path)

# Шаг 2: Подготовка данных
# Обрезаем DEM по границам реки для уменьшения вычислительных затрат.
geoms = river_gdf.geometry.values.tolist()
out_image, out_transform = mask(dem_dataset, geoms, crop=True)
out_meta = dem_dataset.meta.copy()
out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

# Шаг 3: Моделирование гидродинамики
# Для простоты используем метод порогового значения для определения зон подтопления.
threshold = 50  # Пороговое значение высоты для подтопления (в метрах)
flooded_area = np.where(out_image < threshold, 1, 0)

# Преобразование массива в GeoDataFrame
from rasterio.features import shapes

results = (
    {'properties': {'raster_val': v}, 'geometry': s}
    for i, (s, v) in enumerate(
        shapes(flooded_area, mask=flooded_area == 1, transform=out_transform)))

geoms = list(results)
flood_gdf = gpd.GeoDataFrame.from_features(geoms)

# Шаг 4: Оценка рисков
# В данном примере мы просто определяем зоны подтопления.
# Для более точной оценки можно использовать модели гидродинамики, такие как FLO-2D или HEC-RAS.

# Шаг 5: Визуализация результатов
# Создание интерактивной карты с использованием folium
m = folium.Map(location=[river_gdf.centroid.y.mean(), river_gdf.centroid.x.mean()], zoom_start=12)

# Добавление реки на карту
folium.GeoJson(river_gdf).add_to(m)

# Добавление зон подтопления на карту
folium.GeoJson(flood_gdf, style_function=lambda x: {'fillColor': 'blue', 'color': 'blue'}).add_to(m)

# Сохранение карты в файл
m.save("23.html")