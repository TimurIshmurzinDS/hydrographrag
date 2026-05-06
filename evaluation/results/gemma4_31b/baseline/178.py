import folium
import networkx as nx
import matplotlib.pyplot as plt

def calculate_strahler_order(graph):
    """
    Вычисляет порядок Стрлера для каждого ребра в графе.
    Предполагается, что граф направлен от истока к устью.
    """
    orders = {}
    # Находим истоки (узлы без входящих ребер)
    sources = [node for node in graph.nodes() if graph.in_degree(node) == 0]
    
    # Очередь для обхода (BFS)
    queue = sources
    processed_nodes = set()
    
    # Храним входящие порядки для каждого узла
    node_incoming_orders = {node: [] for node in graph.nodes()}
    
    # Для упрощения в синтетическом примере используем итеративный подход
    # В реальном GIS-анализе используется рекурсивный обход от листьев к корню
    nodes_sorted = list(nx.topological_sort(graph))
    
    node_orders = {} # Порядок потока, выходящего из узла
    
    for node in nodes_sorted:
        incoming = list(graph.predecessors(node))
        if not incoming:
            # Исток
            current_order = 1
        else:
            # Получаем порядки всех входящих притоков
            incoming_orders = [node_orders[p] for p in incoming]
            max_order = max(incoming_orders)
            # Если есть два или более потока максимального порядка, порядок увеличивается
            if incoming_orders.count(max_order) >= 2:
                current_order = max_order + 1
            else:
                current_order = max_order
        
        node_orders[node] = current_order
        
        # Присваиваем порядок ребрам, выходящим из этого узла
        for successor in graph.successors(node):
            orders[(node, successor)] = current_order
            
    return orders

# 1. Создание синтетических данных для реки Тентек и её притоков
# Координаты (примерные для демонстрации топологии)
# Структура: { 'NodeName': (lat, lon) }
nodes_coords = {
    'Mouth': (52.1, 85.5),
    'Main_1': (52.2, 85.3),
    'Main_2': (52.3, 85.1),
    'Main_3': (52.4, 84.9),
    'Trib_A1': (52.3, 85.4),
    'Trib_A2': (52.4, 85.5),
    'Trib_B1': (52.4, 85.2),
    'Trib_B2': (52.5, 85.3),
    'Trib_C1': (52.5, 84.8),
    'Trib_C2': (52.6, 84.7),
    'Trib_C3': (52.6, 84.9),
}

# Определение связей (от истока к устью)
edges = [
    ('Main_3', 'Main_2'), ('Main_2', 'Main_1'), ('Main_1', 'Mouth'), # Главное русло
    ('Trib_A2', 'Trib_A1'), ('Trib_A1', 'Main_1'),                 # Приток A
    ('Trib_B2', 'Trib_B1'), ('Trib_B1', 'Main_2'),                 # Приток B
    ('Trib_C2', 'Trib_C1'), ('Trib_C3', 'Trib_C1'), ('Trib_C1', 'Main_3') # Приток C
]

# 2. Построение графа
G = nx.DiGraph()
G.add_edges_from(edges)

# 3. Расчет топологических характеристик
strahler_orders = calculate_strahler_order(G)

# 4. Визуализация с помощью folium
m = folium.Map(location=[52.3, 85.2], zoom_start=8, tiles='CartoDB positron')

# Цвета в зависимости от порядка Стрлера
color_map = {
    1: '#ADD8E6', # Светло-голубой
    2: '#87CEEB', # Небесно-голубой
    3: '#4682B4', # Стальной голубой
    4: '#0000FF'  # Синий
}

for edge, order in strahler_orders.items():
    start_node, end_node = edge
    start_coord = nodes_coords[start_node]
    end_coord = nodes_coords[end_node]
    
    # Толщина линии зависит от порядка
    weight = order * 3
    color = color_map.get(order, 'blue')
    
    folium.PolyLine(
        locations=[start_coord, end_coord],
        color=color,
        weight=weight,
        opacity=0.8,
        tooltip=f"Order: {order}"
    ).add_to(m)

# Добавление маркеров узлов
for node, coord in nodes_coords.items():
    folium.CircleMarker(
        location=coord,
        radius=3,
        color='black',
        fill=True,
        popup=node
    ).add_to(m)

# Сохранение карты
m.save("178.html")

print("Modeling complete. The river network topology has been analyzed and saved to 178.html")