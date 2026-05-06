import folium
from folium.plugins import HeatMap
import numpy as np

# Шаг 1: Сбор данных о реке Кумбель (предположим, что мы имеем координаты точек на карте)
points = [
    [55.7558, 37.6173],  # Москва
    [54.9842, 39.8205],  # Рязань
    [53.9106, 49.4167],  # Пермь
    [52.5200, 13.4050],  # Берлин
]

# Шаг 2: Создание сетчатой структуры с помощью алгоритма Ворона (Voronoi)
def voronoi(points):
    x = np.array([point[1] for point in points])
    y = np.array([point[0] for point in points])
    return Voronoi(np.column_stack((x, y)))

vor = voronoi(points)

# Шаг 3: Визуализация сетки на карте с помощью библиотеки Folium
m = folium.Map(location=[55.7558, 37.6173], zoom_start=6)
folium.Polygon(vor.vertices).add_to(m)

# Сохранение карты в файл
m.save("251.html")