import rasterio
from rasterio.transform import Affine
import numpy as np
import pandas as pd
import folium

# 1. Загрузка данных о потреблении воды
data = pd.read_csv("water_consumption_data.csv")

# 2. Форматирование данных
x = data["longitude"]
y = data["latitude"]
values = data["water_consumption"]

# 3. Создание растровой модели
xmin, xmax, ymin, ymax = np.min(x), np.max(x), np.min(y), np.max(y)
width = int((xmax - xmin) * 1000)
height = int((ymax - ymin) * 1000)

transform = Affine(xmin, (xmax - xmin) / width, 0, ymin, 0, (ymax - ymin) / height)

raster_data = np.zeros((height, width))

# 4. Интерполяция данных
from scipy.interpolate import griddata

grid_x, grid_y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
interpolated_values = griddata((x, y), values, (grid_x, grid_y), method='linear')

raster_data = interpolated_values.reshape(height, width)

# 5. Сохранение растровой модели
with rasterio.open("water_consumption.tif", "w", driver="GTiff", height=height, width=width, count=1, dtype=raster_data.dtype, crs="EPSG:4326", transform=transform) as dst:
    dst.write(raster_data, 1)

# 6. Визуализация результатов
m = folium.Map(location=[np.mean([ymin, ymax]), np.mean([xmin, xmax])], zoom_start=10)

folium.GeoJson("water_consumption.tif", name="Water Consumption").add_to(m)

m.save("115.html")