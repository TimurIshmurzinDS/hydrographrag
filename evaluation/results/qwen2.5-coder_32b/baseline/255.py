import numpy as np
import rasterio
from rasterio.plot import show
import folium
from branca.colormap import LinearColormap

# Шаг 1: Загрузка данных о рельефе (DEM)
dem_path = 'path_to_your_dem_file.tif'  # Укажите путь к вашему файлу DEM
with rasterio.open(dem_path) as src:
    dem_data = src.read(1)

# Шаг 2: Обработка данных
# Нормализация данных рельефа для создания текстуры хлеба
dem_min, dem_max = np.min(dem_data), np.max(dem_data)
normalized_dem = (dem_data - dem_min) / (dem_max - dem_min)

# Шаг 3: Создание текстуры хлеба
# Используем нормализованные данные для создания цветовой карты, имитирующей рельеф
colormap = LinearColormap(['saddlebrown', 'burlywood', 'wheat'], vmin=0, vmax=1)
texture = colormap(normalized_dem)

# Шаг 4: Визуализация на карте с использованием folium
# Получение границ изображения для центрирования карты
bounds = src.bounds
m = folium.Map(location=[(bounds.top + bounds.bottom) / 2, (bounds.right + bounds.left) / 2], zoom_start=10)

# Добавление текстуры на карту
folium.raster_layers.ImageOverlay(
    image=texture,
    bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
    opacity=0.7,
    interactive=True,
    cross_origin=False,
    zindex=1
).add_to(m)

# Добавление цветовой карты для легенды
colormap.add_to(m)

# Сохранение карты в файл
m.save("255.html")