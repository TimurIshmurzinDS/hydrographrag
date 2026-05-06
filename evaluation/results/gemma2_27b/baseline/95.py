import geopandas as gpd
from networkx import DiGraph, shortest_path
import folium

# Загрузка данных о реках из Shapefile
rivers = gpd.read_file("rivers.shp")

# Создание графа
graph = DiGraph()

# Добавление вершин (точек слияния) в граф
for index, row in rivers.iterrows():
    graph.add_node(index, pos=(row.geometry.x, row.geometry.y))

# Добавление ребер (участков рек) в граф
for index, row in rivers.iterrows():
    if row["downstream"] != -1:  # Проверка наличия downstream реки
        graph.add_edge(index, row["downstream"])

# Поиск кратчайшего пути от Улькен Алматы к Шыжын
path = shortest_path(graph, source=rivers[rivers["name"] == "Улькен Алматы"].index[0], target=rivers[rivers["name"] == "Шыжын"].index[0])

# Визуализация пути на карте
m = folium.Map(location=[43.25, 76.95], zoom_start=10)

for i in range(len(path)-1):
    folium.PolyLine([rivers.loc[path[i]].geometry, rivers.loc[path[i+1]].geometry], color="blue").add_to(m)

# Сохранение карты
m.save("95.html")