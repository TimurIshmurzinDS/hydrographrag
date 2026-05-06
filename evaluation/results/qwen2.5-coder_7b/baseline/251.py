import folium
from folium.plugins import Graph

# Пример данных о гидрографической сети реки Кумбель (замените на реальные данные)
edges = [
    ('A', 'B'),
    ('B', 'C'),
    ('C', 'D'),
    ('D', 'E'),
    ('E', 'F'),
    ('F', 'G'),
    ('G', 'H'),
    ('H', 'I'),
    ('I', 'J'),
    ('J', 'K')
]

# Координаты узлов (замените на реальные данные)
node_coords = {
    'A': [51.234, 6.789],
    'B': [51.235, 6.790],
    'C': [51.236, 6.791],
    'D': [51.237, 6.792],
    'E': [51.238, 6.793],
    'F': [51.239, 6.794],
    'G': [51.240, 6.795],
    'H': [51.241, 6.796],
    'I': [51.242, 6.797],
    'J': [51.243, 6.798],
    'K': [51.244, 6.799]
}

# Создание карты
m = folium.Map(location=[node_coords['A'][0], node_coords['A'][1]], zoom_start=12)

# Добавление узлов на карту
for node, coords in node_coords.items():
    folium.Marker(coords, popup=node).add_to(m)

# Создание графа и добавление его на карту
graph = Graph()
for edge in edges:
    start_node, end_node = edge
    start_coords = node_coords[start_node]
    end_coords = node_coords[end_node]
    graph.add_edge(start_node, end_node, weight=1.0)
    folium.PolyLine([start_coords, end_coords], color='blue', weight=2).add_to(m)

# Сохранение карты
m.save("251.html")