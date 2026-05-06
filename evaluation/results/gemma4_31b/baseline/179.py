import folium
import networkx as nx
from shapely.geometry import LineString, Point
import geopandas as gpd
import pandas as pd

# 1. Симуляция данных речной сети (так как реальный shape-файл отсутствует)
# Создаем синтетическую сеть, где Киши-Осек является одним из истоков
# Координаты условны (Центральная Азия/Сибирь стиль)
data = [
    {"id": 1, "name": "Kishi-Osek", "coords": [(70.1, 45.1), (70.2, 45.2)]},
    {"id": 2, "name": "Segment_A", "coords": [(70.2, 45.2), (70.3, 45.3)]},
    {"id": 3, "name": "Segment_B", "coords": [(70.2, 45.2), (70.1, 45.3)]},
    {"id": 4, "name": "Main_River_1", "coords": [(70.3, 45.3), (70.4, 45.4)]},
    {"id": 5, "name": "Main_River_2", "coords": [(70.1, 45.3), (70.4, 45.4)]},
    {"id": 6, "name": "Downstream_1", "coords": [(70.4, 45.4), (70.5, 45.5)]},
    {"id": 7, "name": "Downstream_2", "coords": [(70.5, 45.5), (70.6, 45.6)]},
    {"id": 8, "name": "Tributary_X", "coords": [(70.3, 45.1), (70.3, 45.3)]}, # Приток, не должен быть затронут
]

# 2. Построение направленного графа
G = nx.DiGraph()

river_segments = []
for seg in data:
    start_node = tuple(seg["coords"][0])
    end_node = tuple(seg["coords"][1])
    G.add_edge(start_node, end_node, id=seg["id"], name=seg["name"])
    river_segments.append({
        "id": seg["id"],
        "name": seg["name"],
        "geometry": LineString(seg["coords"])
    })

# Создаем GeoDataFrame для удобства работы с геометрией
gdf_rivers = gpd.GeoDataFrame(river_segments)

# 3. Выявление путей распространения паводка
# Определяем стартовую точку (начало реки Киши-Осек)
start_river_name = "Kishi-Osek"
start_node = None

# Ищем узел, с которого начинается река Киши-Осек
for u, v, attr in G.edges(data=True):
    if attr['name'] == start_river_name:
        start_node = u
        break

if start_node:
    # Находим все узлы, которые находятся ниже по течению (потомки в графе)
    affected_nodes = nx.descendants(G, start_node)
    affected_nodes.add(start_node) # Добавляем саму точку старта
    
    # Определяем ребра (участки рек), которые затронуты
    affected_edges = []
    for u, v, attr in G.edges(data=True):
        if u in affected_nodes:
            affected_edges.append(attr['id'])
else:
    affected_edges = []

# 4. Визуализация с помощью folium
# Центрируем карту по средней точке сети
m = folium.Map(location=[45.3, 70.3], zoom_start=7, tiles="CartoDB positron")

for index, row in gdf_rivers.iterrows():
    # Определяем цвет: красный если в зоне паводка, синий если нет
    color = "red" if row['id'] in affected_edges else "blue"
    weight = 4 if row['id'] in affected_edges else 2
    opacity = 0.8 if row['id'] in affected_edges else 0.4
    
    # Преобразуем координаты LineString в формат folium [[lat, lon], ...]
    coords = [[p[1], p[0]] for p in row['geometry'].coords]
    
    folium.PolyLine(
        locations=coords,
        color=color,
        weight=weight,
        opacity=opacity,
        tooltip=f"River: {row['name']} {'(Flood Path)' if row['id'] in affected_edges else ''}"
    ).add_to(m)

# Добавляем маркер истока
start_coords = [45.1, 70.1] # Соответствует Киши-Осек
folium.Marker(
    location=start_coords, 
    popup="Исток паводка: р. Киши-Осек", 
    icon=folium.Icon(color='darkred', icon='info-sign')
).add_to(m)

# Сохранение карты
m.save("179.html")

print("Modeling complete. The map has been saved as 179.html")