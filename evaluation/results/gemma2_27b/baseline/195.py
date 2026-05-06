import rasterio
from rasterio.plot import show
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import folium

# Загрузка данных
soil_raster = rasterio.open("path/to/soil_data.tif")
rivers_vector = gpd.read_file("path/to/river_data.shp")
canals_vector = gpd.read_file("path/to/canal_data.shp")

# Расчет расстояния до рек и каналов
rivers_distance = rivers_vector.geometry.apply(lambda x: np.min([np.linalg.norm(x.coords[0] - p) for p in soil_raster.xy])
canals_distance = canals_vector.geometry.apply(lambda x: np.min([np.linalg.norm(x.coords[0] - p) for p in soil_raster.xy])

# Определение типа почвы (заменить на реальные типы почв и их склонность к засолению)
soil_type = np.array([1 if i == 1 else 0 for i in soil_raster.read(1)])

# Расчет риска засоления (примерная модель, заменить на более точную)
risk = 0.5 * rivers_distance + 0.3 * canals_distance + 0.2 * soil_type

# Визуализация на карте Folium
m = folium.Map(location=[45.18, 63.1], zoom_start=12)
folium.GeoJson("path/to/river_data.shp").add_to(m)
folium.GeoJson("path/to/canal_data.shp").add_to(m)

# Добавление слоя риска засоления
risk_layer = folium.FeatureGroup(name="Risk")
for i in range(len(risk)):
    folium.CircleMarker(location=soil_raster.xy[i], radius=5, color='red' if risk[i] > 0.8 else 'yellow' if risk[i] > 0.5 else 'green').add_to(risk_layer)

risk_layer.add_to(m)
folium.LayerControl().add_to(m)

# Сохранение карты
m.save("195.html")