import osmnx as ox
import networkx as nx
import folium
from geopy.distance import geodesic

def solve_river_connectivity():
    # 1. Настройка параметров поиска
    # Определяем регион (Восточный Казахстан), где протекают эти реки
    place_name = "East Kazakhstan Region, Kazakhstan"
    
    print("Загрузка речной сети из OpenStreetMap... Это может занять время.")
    # Загружаем только водные пути (waterways)
    # Мы используем custom_filter, чтобы получить именно реки и ручьи
    graph = ox.graph_from_place(
        place_name, 
        network_type='all', 
        custom_filter='["waterway"~"river|stream"]'
    )

    # 2. Поиск узлов, относящихся к конкретным рекам
    # В OSM названия могут быть на разных языках, поэтому ищем по ключевым словам
    nodes_tekes = []
    nodes_tentek = []

    for u, v, data in graph.edges(data=True):
        name = data.get('name', '').lower()
        if 'текес' in name or 'tekes' in name:
            nodes_tekes.extend([u, v])
        if 'тентек' in name or 'tentek' in name:
            nodes_tentek.extend([u, v])

    if not nodes_tekes or not nodes_tentek:
        print("Ошибка: Не удалось найти одну из рек в базе данных OSM.")
        return

    # Убираем дубликаты
    nodes_tekes = list(set(nodes_tekes))
    nodes_tentek = list(set(nodes_tentek))

    # 3. Поиск кратчайшего пути между двумя множествами узлов
    # Находим пару узлов (один из Текес, один из Тентек), расстояние между которыми минимально по графу
    min_dist = float('inf')
    best_path = []

    # Для оптимизации берем по одному репрезентативному узлу (например, средние или случайные)
    # или перебираем, если граф небольшой.
    source_node = nodes_tekes[0]
    target_node = nodes_tentek[0]

    try:
        # Вычисляем кратчайший путь по весам (длине ребер)
        path = nx.shortest_path(graph, source=source_node, target=target_node, weight='length')
        path_length = nx.shortest_path_length(graph, source=source_node, target=target_node, weight='length')
    except nx.NetworkXNoPath:
        print("Путь между реками в графе не найден. Возможно, сеть фрагментирована.")
        return

    print(f"Общая протяженность речной сети между Текес и Тентек: {path_length / 1000:.2f} км")

    # 4. Визуализация
    # Создаем карту, центрированную по одной из точек
    start_coords = graph.nodes[source_node]
    m = folium.Map(location=[start_coords['y'], start_coords['x']], zoom_start=7, tiles='CartoDB positron')

    # Извлекаем координаты всех узлов пути для отрисовки линии
    path_coords = []
    for node in path:
        node_data = graph.nodes[node]
        path_coords.append([node_data['y'], node_data['x']])

    # Добавляем линию пути на карту
    folium.PolyLine(path_coords, color="blue", weight=3, opacity=0.8, tooltip="Речной путь").add_to(m)
    
    # Маркеры для начала и конца
    folium.Marker([start_coords['y'], start_coords['x']], popup="Река Текес", icon=folium.Icon(color='green')).add_to(m)
    end_coords = graph.nodes[target_node]
    folium.Marker([end_coords['y'], end_coords['x']], popup="Река Тентек", icon=folium.Icon(color='red')).add_to(m)

    # Сохранение карты
    m.save("167.html")
    print("Карта сохранена в файл 167.html")

if __name__ == "__main__":
    # Установка необходимых библиотек перед запуском:
    # pip install osmnx networkx folium geopy
    solve_river_connectivity()