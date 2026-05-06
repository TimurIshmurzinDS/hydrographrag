import networkx as nx
import folium
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Вычисляет расстояние между двумя точками на сфере (формула гаверсинуса).
    """
    # Радиус Земли в километрах
    R = 6371.0 
    
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    return R * c

# 1. Создание синтетических данных речной сети (имитация ГИС-данных)
# В реальном сценарии здесь будет загрузка Shapefile или GeoJSON
# Координаты (примерные для демонстрации топологии)
nodes = {
    "Shyzyn_Start": (68.12, 49.55),
    "Node_A": (68.25, 49.60),
    "Node_B": (68.40, 49.65),
    "Node_C": (68.50, 49.70),
    "Dos_End": (68.70, 49.80)
}

# Определение связей (ребер) между узлами
edges = [
    ("Shyzyn_Start", "Node_A"),
    ("Node_A", "Node_B"),
    ("Node_B", "Node_C"),
    ("Node_C", "Dos_End"),
    ("Node_A", "Node_C") # Альтернативный путь (приток)
]

# 2. Построение взвешенного графа
G = nx.Graph()

for edge in edges:
    u, v = edge
    coord_u = nodes[u]
    coord_v = nodes[v]
    
    # Расчет реального расстояния между узлами в км
    dist = haversine(coord_u[0], coord_u[1], coord_v[0], coord_v[1])
    G.add_edge(u, v, weight=dist)

# 3. Расчет пути от реки Шыжын до реки Дос
start_node = "Shyzyn_Start"
end_node = "Dos_End"

try:
    path = nx.shortest_path(G, source=start_node, target=end_node, weight='weight')
    total_length = nx.shortest_path_length(G, source=start_node, target=end_node, weight='weight')
    
    print(f"Маршрут: {' -> '.join(path)}")
    print(f"Общая длина речного пути: {total_length:.2f} км")

    # 4. Визуализация на карте
    # Центрируем карту по начальной точке
    m = folium.Map(location=nodes["Shyzyn_Start"], zoom_start=9)

    # Создаем список координат для отрисовки линии
    path_coords = [nodes[node] for node in path]
    
    # Добавляем линию пути на карту
    folium.PolyLine(path_coords, color="blue", weight=3, opacity=0.8, tooltip="Речной путь").add_to(m)

    # Добавляем маркеры начала и конца
    folium.Marker(nodes[start_node], popup="Река Шыжын", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(nodes[end_node], popup="Река Дос", icon=folium.Icon(color='red')).add_to(m)

    # Сохранение карты
    m.save("100.html")
    print("Карта успешно сохранена в файл 100.html")

except nx.NetworkXNoPath:
    print("Путь между указанными реками не найден.")