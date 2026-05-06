import os
from osgeo import gdal
import numpy as np
import networkx as nx
from scipy import ndimage
import folium

# Загрузите данные о рельефе местности в формате GeoTIFF.
ds = gdal.Open('relief.tif')
dem = ds.ReadAsArray()

# Создайте сетку для моделирования водного потока с помощью алгоритма D8.
cell_size = 10
dem_resampled = ndimage.zoom(dem, (1/cell_size, 1/cell_size), order=0)

# Определите реки Эмель и Тентек на основе данных о гидрографии или используя алгоритмы обнаружения речной сети.
river_emel = np.zeros_like(dem_resampled)
river_tentek = np.zeros_like(dem_resampled)

# Используйте результаты моделирования водного потока для определения точек пересечения водоразделов между двумя реками.
G = nx.Graph()
for i in range(dem_resampled.shape[0]):
    for j in range(dem_resampled.shape[1]):
        if dem_resampled[i, j] > 100:
            G.add_node((i, j))
            neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
            for neighbor in neighbors:
                if 0 <= neighbor[0] < dem_resampled.shape[0] and 0 <= neighbor[1] < dem_resampled.shape[1]:
                    G.add_edge((i, j), neighbor)

river_emel_nodes = []
river_tentek_nodes = []

for node in G.nodes():
    if river_emel[node[0], node[1]] == 0:
        river_emel_nodes.append(node)
    elif river_tentek[node[0], node[1]] == 0:
        river_tentek_nodes.append(node)

intersection_points = []
for point in river_emel_nodes:
    for other_point in river_tentek_nodes:
        if np.isclose(point, other_point).all():
            intersection_points.append(point)

# Визуализируйте результат на карте с помощью библиотеки folium.
m = folium.Map(location=[55.0, 80.0], zoom_start=10)
folium.Marker([intersection_points[0][0]*cell_size, intersection_points[0][1]*cell_size], popup='Пересечение водоразделов').add_to(m)

for point in intersection_points:
    folium.CircleMarker([point[0]*cell_size, point[1]*cell_size], radius=5).add_to(m)

m.save("174.html")