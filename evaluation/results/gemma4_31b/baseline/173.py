import folium
import networkx as nx

def solve_river_flow():
    # 1. Создание топологической сети (Граф)
    # В реальном сценарии данные загружаются из Shapefile или GeoJSON
    # Здесь мы моделируем сеть: Шынжалы -> Приток -> Основная река -> Бассейн
    
    # Координаты узлов (примерные координаты для демонстрации топологии)
    # Формат: 'Node_ID': (Latitude, Longitude)
    nodes = {
        'Shynzhaly_Source': (50.123, 65.456),
        'Shynzhaly_Mid': (50.100, 65.500),
        'Confluence_A': (50.050, 65.550), # Слияние с притоком
        'Main_River_Start': (49.900, 65.600), # Впадение в основную систему
        'Main_River_Mid': (49.700, 65.700),
        'Main_River_End': (49.500, 65.800)   # Конечный сток (бассейн)
    }

    # Определение направленных ребер (откуда -> куда)
    # Это и есть топология сети стока
    edges = [
        ('Shynzhaly_Source', 'Shynzhaly_Mid'),
        ('Shynzhaly_Mid', 'Confluence_A'),
        ('Confluence_A', 'Main_River_Start'),
        ('Main_River_Start', 'Main_River_Mid'),
        ('Main_River_Mid', 'Main_River_End')
    ]

    # Создание направленного графа NetworkX
    G = nx.DiGraph()
    G.add_nodes_from(nodes.keys())
    G.add_edges_from(edges)

    # 2. Анализ направления стока
    # Определяем путь от реки Шынжалы до конечной системы
    start_node = 'Shynzhaly_Source'
    end_node = 'Main_River_End'
    
    try:
        flow_path = nx.shortest_path(G, source=start_node, target=end_node)
    except nx.NetworkXNoPath:
        print("Путь стока не найден")
        return

    # 3. Визуализация с помощью folium
    # Центрируем карту по первой точке
    start_coords = nodes[start_node]
    m = folium.Map(location=start_coords, zoom_start=8, tiles='CartoDB positron')

    # Добавляем узлы на карту
    for node_id, coords in nodes.items():
        color = 'blue' if node_id == 'Shynzhaly_Source' else 'red' if node_id == 'Main_River_End' else 'gray'
        folium.CircleMarker(
            location=coords,
            radius=5,
            popup=node_id,
            color=color,
            fill=True,
            fill_color=color
        ).add_to(m)

    # Рисуем линию стока (путь по топологии)
    path_coords = [nodes[node] for node in flow_path]
    
    # Создаем полилинию для отображения направления стока
    folium.PolyLine(
        locations=path_coords,
        color='blue',
        weight=4,
        opacity=0.8,
        tooltip="Направление стока от р. Шынжалы"
    ).add_to(m)

    # Добавляем стрелки (имитация) через текстовые маркеры в середине сегментов
    for i in range(len(path_coords) - 1):
        p1 = path_coords[i]
        p2 = path_coords[i+1]
        mid_point = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]
        folium.Marker(
            location=mid_point,
            icon=folium.DivIcon(html=f'<div style="font-size: 12pt; color: blue;">&rarr;</div>'),
            icon_anchor=(0, 0)
        ).add_to(m)

    # Сохранение результата
    m.save("173.html")
    print("Анализ завершен. Карта сохранена в файл 173.html")

if __name__ == "__main__":
    solve_river_flow()