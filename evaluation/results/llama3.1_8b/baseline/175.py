import networkx as nx
import folium

# Данные о речной сети (предположим, что они хранятся в формате CSV)
river_data = {
    'Сарыкан': [
        {'name': 'Устье', 'lat': 55.1234, 'lon': 36.5678},
        {'name': 'Пруд', 'lat': 55.2345, 'lon': 37.6789},
        {'name': 'Водопад', 'lat': 55.3456, 'lon': 38.7890}
    ]
}

# Создаем граф речной сети
G = nx.Graph()

# Добавляем узлы графа (участки реки)
for i, segment in enumerate(river_data['Сарыкан']):
    G.add_node(segment['name'], lat=segment['lat'], lon=segment['lon'])

# Добавляем ребра графа (связи между участками реки)
G.add_edge('Устье', 'Пруд')
G.add_edge('Пруд', 'Водопад')

# Рассчитываем коэффициент связности
connectivity_coefficient = nx.clustering(G)

print(f"Коэффициент связности: {connectivity_coefficient}")

# Создаем карту с маркерами для каждого участка реки
m = folium.Map(location=[55.1234, 36.5678], zoom_start=10)
for node in G.nodes():
    folium.Marker([G.nodes[node]['lat'], G.nodes[node]['lon']], popup=node).add_to(m)

# Сохраняем карту в файл
m.save("175.html")