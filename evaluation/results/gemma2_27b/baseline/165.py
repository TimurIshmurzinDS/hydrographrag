import rasterio
from rasterio.plot import show
import folium
import matplotlib.pyplot as plt

# Загрузка DEM
dem = rasterio.open('path/to/DEM.tif')

# Загрузка данных о гидрологии (уровни воды, осадки)
hydrology_data = ... # Загрузить данные из CSV или NetCDF

# Гидравлическое моделирование (использовать библиотеку Hydrology или GDAL)
flow_accumulation = ... # Рассчитать поток воды на основе DEM и hydrology_data

# Создание карты Folium
m = folium.Map(location=[40, 60], zoom_start=10)

# Визуализация уровня воды (риск паводка)
plt.imshow(flow_accumulation)
folium.rasterio.show_image(flow_accumulation, bounds=(dem.bounds), name="Flow Accumulation")

m.save("165.html")