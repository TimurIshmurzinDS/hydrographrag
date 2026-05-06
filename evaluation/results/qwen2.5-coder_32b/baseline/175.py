import geopandas as gpd
import networkx as nx
from shapely.geometry import LineString, Point
import folium

# Шаг 1: Подготовка данных
# Предположим, что у нас есть файл shapefile с речной сетью
river_network = gpd.read_file('path_to_shapefile.shp')

# Шаг 2: Построение графа речной сети
G = nx.Graph()

# Добавление ребер в граф
for index, row in river_network.iterrows():
    line = row['geometry']
    coords = list(line.coords)
    for i in range(len(coords) - 1):
        G.add_edge(Point(coords[i]), Point(coords[i + 1]))

# Шаг 3: Расчет коэффициента связности
# Глобальный коэффициент кластеризации
global_clustering_coefficient = nx.average_clustering(G)
print(f"Глобальный коэффициент кластеризации: {global_clustering_coefficient}")

# Средняя длина пути между вершинами
average_shortest_path_length = nx.average_shortest_path_length(G)
print(f"Средняя длина пути между вершинами: {average_shortest_path_length}")

# Коэффициент связности можно определить как отношение глобального коэффициента кластеризации к средней длине пути
connectivity_coefficient = global_clustering_coefficient / average_shortest_path_length
print(f"Коэффициент связности: {connectivity_coefficient}")

# Шаг 4: Визуализация результата
# Создание карты с использованием folium
m = folium.Map(location=[river_network.centroid.y.mean(), river_network.centroid.x.mean()], zoom_start=10)

# Добавление линий рек на карту
for index, row in river_network.iterrows():
    line = row['geometry']
    coords = list(line.coords)
    folium.PolyLine(locations=coords, color='blue', weight=2.5).add_to(m)

# Сохранение карты в файл
m.save("175.html")