import geopandas as gpd
import rasterio
from rasterio.mask import mask
import numpy as np
import folium
from shapely.geometry import shape

# Шаг 1: Сбор данных
# Предположим, что у нас есть DEM (Digital Elevation Model) и геометрия бассейна реки в формате GeoJSON.
dem_path = 'path_to_dem.tif'
shynzhaly_basin_path = 'path_to_shynzhaly_basin.geojson'

# Шаг 2: Подготовка данных
# Загрузка DEM и геометрии бассейна реки
dem_dataset = rasterio.open(dem_path)
basin_gdf = gpd.read_file(shynzhaly_basin_path)

# Обрезка DEM по границам бассейна реки
geoms = [shape(basin_gdf.geometry.iloc[0])]
out_image, out_transform = mask(dem_dataset, geoms, crop=True)
elevation = out_image[0]

# Шаг 3: Моделирование
# Простая модель для демонстрации: определение зон затопления при заданном уровне воды.
flood_level = elevation.min() + 10  # Уровень воды выше минимального уровня на 10 единиц
flood_mask = elevation < flood_level

# Шаг 4: Анализ результатов
# Преобразование маски затопления в геоданные для визуализации
flood_array = np.where(flood_mask, 1, 0)
flood_raster = rasterio.open(
    'memory',
    'w+',
    driver='GTiff',
    height=flood_array.shape[0],
    width=flood_array.shape[1],
    count=1,
    dtype=rasterio.uint8,
    crs=dem_dataset.crs,
    transform=out_transform
)
flood_raster.write(flood_array, 1)

# Шаг 5: Визуализация
# Создание интерактивной карты с использованием folium
m = folium.Map(location=[basin_gdf.centroid.y.iloc[0], basin_gdf.centroid.x.iloc[0]], zoom_start=12)

# Добавление границ бассейна реки на карту
folium.GeoJson(basin_gdf).add_to(m)

# Добавление зон затопления на карту
flood_raster = rasterio.open('memory')
flooding_layer = folium.raster_layers.ImageOverlay(
    image=flood_array,
    bounds=[[out_transform.yoff, out_transform.xoff], [out_transform.yoff + out_transform.height * out_transform.a, out_transform.xoff + out_transform.width * out_transform.a]],
    opacity=0.5
)
flooding_layer.add_to(m)

# Сохранение карты в файл
m.save("161.html")