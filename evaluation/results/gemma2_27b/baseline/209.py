import rasterio
from rasterstats import zonal_stats
import numpy as np
import HydroPy
import folium

# Загрузка DEM
dem = rasterio.open('Urzhar_DEM.tif')
elevation = dem.read(1)

# Расчет параметров водосбора
slope, aspect = np.gradient(elevation)

# Определение сценария экстремальных осадков (пример)
rainfall = 100 # мм/день

# Гидравлическое моделирование
model = HydroPy.Model('Urzhar_River')
model.add_rainfall(rainfall)
model.run()

# Оценка риска наводнения
flood_zone = model.get_flood_zone()

# Визуализация на карте
m = folium.Map(location=[45, 60], zoom_start=10)
folium.GeoJson(flood_zone).add_to(m)
m.save("209.html")