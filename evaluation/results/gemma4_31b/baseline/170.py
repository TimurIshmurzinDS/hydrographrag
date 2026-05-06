import folium
import networkx as nx
import geopandas as gpd
from shapely.geometry import LineString, Point

# 1. Симуляция данных гидрографии (так как реальный shape-файл Терисбутака недоступен)
# Создаем синтетическую сеть: Терисбутак -> Река А -> Река Б -> Главная Артерия
data = [
    {"name": "Ручей Терисбутак", "coords": [(70.1, 45.1), (70.2, 45.2)], "order": 1},
    {"name": "Река А", "coords": [(70.2, 45.2), (70.4, 45.4)], "order": 2},
    {"name": "Река Б", "coords": [(70.4, 45.4), (70.7, 45.6)], "order": 3},
    {"name": "Главная Артерия", "coords": [(70.7, 45.6), (71.5, 46.0)], "order": 4},
    # Добавим соседние притоки для полноты сети
    {"name": "Приток 1", "coords": [(70.0, 45.3), (70.2, 45.2)], "order": 1},
    {"name": "Приток 2", "coords": [(70.5, 45.3), (70.4, 45.4)], "order": 2},
]

# Создание GeoDataFrame
lines = []
for item in data:
    lines.append({
        'name': item['name'],
        'geometry': LineString(item['coords']),
        'order': item['order']
    })

gdf = gpd.GeoDataFrame(lines)

# 2. Построение графа для анализа иерархии
G = nx.DiGraph()

for idx, row in gdf.iterrows():
    coords = list(row.geometry.coords)
    start_node = coords[0]
    end_node = coords[-1]
    G.add_edge(start_node, end_node, name=row['name'], order=row['order'])

# 3. Трассировка от Терисбутака до главной артерии
def trace_river_hierarchy(graph, start_river_name):
    # Находим начальный узел ручья
    start_node = None
    for u, v, d in graph.edges(data=True):
        if d['name'] == start_river_name:
            start_node = u
            break
    
    if not start_node:
        return []

    # Поиск пути до самого дальнего узла (основной артерии)
    # В данной задаче идем по направленным ребрам до конца
    path_nodes = [start_node]
    current_node = start_node
    
    while True:
        successors = list(graph.successors(current_node))
        if not successors:
            break
        # В реальной сети может быть разветвление, здесь берем основной поток
        current_node = successors[0]
        path_nodes.append(current_node)
    
    return path_nodes

# Выполняем трассировку
path_nodes = trace_river_hierarchy(G, "Ручей Терисбутак")

# 4. Визуализация с помощью folium
# Центрируем карту по первой точке
m = folium.Map(location=[45.5, 70.5], zoom_start=7, tiles='CartoDB positron')

# Рисуем всю сеть
for idx, row in gdf.iterrows():
    # Определяем цвет и толщину в зависимости от порядка
    weight = row['order'] * 2
    color = 'blue' if row['order'] > 2 else 'lightblue'
    
    # Проверяем, входит ли этот сегмент в наш путь трассировки
    # (упрощенно: если сегмент принадлежит пути от Терисбутака)
    is_in_path = False
    coords = list(row.geometry.coords)
    if coords[0] in path_nodes and coords[-1] in path_nodes:
        is_in_path = True
        color = 'red' # Выделяем путь трассировки красным
        weight += 2

    folium.PolyLine(
        locations=[(lat, lon) for lon, lat in coords], 
        color=color, 
        weight=weight, 
        tooltip=f"{row['name']} (Порядок: {row['order']})"
    ).add_to(m)

# Добавляем маркеры начала и конца
start_coords = (45.1, 70.1)
end_coords = (46.0, 71.5)
folium.Marker(start_coords, popup="Исток: Терисбутак", icon=folium.Icon(color='green')).add_to(m)
folium.Marker(end_coords, popup="Главная Артерия", icon=folium.Icon(color='blue')).add_to(m)

# Сохранение результата
m.save("170.html")

print("Анализ завершен. Карта сохранена в файл 170.html")