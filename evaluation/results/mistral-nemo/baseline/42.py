import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import numpy as np
import folium

# 1. Подготовка данных
fields_data = pd.read_csv('fields.csv')  # Дatos de los campos agrícolas
water_samples = pd.read_csv('water_samples.csv')  # Datos de las muestras de agua

# 2. Геопространственный анализ
geometry = [Point(xy) for xy in zip(water_samples['longitude'], water_samples['latitude'])]
gdf_water = gpd.GeoDataFrame(water_samples, geometry=geometry)
gdf_fields = gpd.read_file('fields.shp')  # Datos de los campos agrícolas en formato shapefile

# Calcular la distancia desde cada muestra de agua hasta el campo agrícola más cercano
distances = gpd.sjoin_nearest(gdf_water, gdf_fields, how='first')
distances['distance'] = distances.apply(lambda row: row.geometry.distance(row.match_index.geometry), axis=1)

# 3. Статистический анализ
# Aquí se puede realizar un análisis estadístico para entender la relación entre la calidad del agua y la distancia a los campos agrícolas

# 4. Визуализация
m = folium.Map(location=[55.7821, 37.6219], zoom_start=10)  # Coordenadas de ejemplo para Moscú

# Agregar puntos de muestra de agua con el nivel de contaminación como tamaño del punto
for _, row in water_samples.iterrows():
    folium.CircleMarker(location=[row['latitude'], row['longitude']],
                        radius=np.log(row['pollution_level'] + 1),
                        color='red',
                        fill=True,
                        fill_opacity=0.5).add_to(m)

# Agregar campos agrícolas como polígonos
for _, row in fields_data.iterrows():
    folium.Polygon([(row['lat'], row['lon'])],
                   color='green',
                   weight=2,
                   fill=True,
                   fill_opacity=0.3).add_to(m)

# 5. Интерпретация результатов
# Aquí se pueden hacer interpretaciones basadas en los resultados obtenidos

# Guardar el mapa como HTML
m.save("42.html")