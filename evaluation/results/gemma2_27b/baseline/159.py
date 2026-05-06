import rasterio
from rasterio.plot import show
import numpy as np
import matplotlib.pyplot as plt
import folium

# 1. Загрузка данных DEM и гидросети
dem = rasterio.open('path_to_DEM.tif')
rivers = rasterio.open('path_to_rivers.shp')

# 2. Расчет таяния снега (примерная модель)
def snowmelt(temperature, elevation):
    return temperature * 0.1 * (30 - elevation / 100)

# 3. Гидравлическое моделирование (примерная реализация)
def flow_model(snowmelt, channel_capacity):
    return np.minimum(snowmelt + channel_capacity, channel_capacity * 2)

# 4. Определение зон риска перелива

# ... (код для расчета уровня воды и сравнения с высотой берегов)

# Визуализация на карте
m = folium.Map(location=[dem.transform[1], dem.transform[0]], zoom_start=12)
folium.GeoJson('path_to_rivers.shp').add_to(m)
# ... (код для визуализации зон риска перелива)

m.save("159.html")