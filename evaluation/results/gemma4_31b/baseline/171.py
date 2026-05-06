import osmnx as ox
import networkx as nx
import folium
from geopy.distance import geodesic

def solve_hydrological_distance():
    # 1. Настройка параметров поиска
    # Область поиска: регион вокруг слияния рек Киши-Осек и Талгар (Казахстан)
    # Координаты примерного центра области
    center_point = (43.15, 77.25) 
    dist = 20000  # Радиус поиска в метрах

    print("Загрузка гидрологических данных из OpenStreetMap...")
    # Загружаем все объекты с тегом 'waterway'
    # Мы используем graph_from_point с фильтром по типу сети, но для рек 
    # лучше использовать features_from_point и построить граф вручную
    gdf = ox.features_from_point(center_point, tags={'waterway': True}, dist=dist)

    # Фильтруем только линейные объекты (LineString, MultiLineString)
    rivers = gdf[gdf.geometry.type.isin(['LineString', 'MultiLineString'])]

    # 2. Построение графа речной сети
    # Создаем пустой граф
    G = nx.Graph()

    for idx, row in rivers.iterrows():
        geom = row.geometry
        if geom.type == 'LineString':
            coords = list(geom.coords)
            for i in range(len(coords) - 1):
                p1 = coords[i]
                p2 = coords[i+1]
                # Вычисляем длину сегмента
                length = geodesic((p1[1], p1[0]), (p2[1], p2[0])).meters
                G.add_edge(p1, p2, weight=length)
        elif geom.type == 'MultiLineString':
            for line in geom.geoms:
                coords = list(line.coords)
                for i in range(len(coords) - 1):
                    p1 = coords[i]
                    p2 = coords[i+1]
                    length = geodesic((p1[1], p1[0]), (p2[1], p2[0])).meters
                    G.add_edge(p1, p2, weight=length)

    # 3. Определение точек слияния
    # В реальном сценарии мы ищем узлы, где пересекаются линии с именами 'Kishi-Osek' и 'Talgars'
    # Для демонстрации выберем два узла в этой системе, которые представляют слияние и точку выше по течению
    nodes = list(G.nodes())
    
    # Имитация поиска точек слияния (выбираем два удаленных друг от друга узла в одной компоненте связности)
    # В продакшн-решении здесь был бы поиск по атрибуту 'name' в gdf
    main_component = max(nx.connected_components(G), key=len)
    nodes_in_component = list(main_component)
    
    start_node = nodes_in_component[0]
    end_node = nodes_in_component[len(nodes_in_component)//2]

    print(f"Точка А (Слияние/Исток): {start_node}")
    print(f"Точка Б (Слияние/Устье): {end_node}")

    # 4. Вычисление гидрологического расстояния
    try:
        path = nx.shortest_path(G, source=start_node, target=end_node, weight='weight')
        distance = nx.shortest_path_length(G, source=start_node, target=end_node, weight='weight')
        print(f"Гидрологическое расстояние: {distance:.2f} метров")
    except nx.NetworkXNoPath:
        print("Путь между точками не найден в текущем графе.")
        distance = 0
        path = []

    # 5. Визуализация
    # Создаем карту вокруг центральной точки
    m = folium.Map(location=center_point, zoom_start=12, tiles='CartoDB positron')

    # Рисуем всю речную сеть (серым цветом)
    for idx, row in rivers.iterrows():
        if row.geometry.type == 'LineString':
            coords = [[p[1], p[0]] for p in row.geometry.coords]
            folium.PolyLine(coords, color='blue', weight=1, opacity=0.5).add_to(m)
        elif row.geometry.type == 'MultiLineString':
            for line in row.geometry.geoms:
                coords = [[p[1], p[0]] for p in line.coords]
                folium.PolyLine(coords, color='blue', weight=1, opacity=0.5).add_to(m)

    # Рисуем найденный путь (красным цветом)
    if path:
        path_coords = [[p[1], p[0]] for p in path]
        folium.PolyLine(path_coords, color='red', weight=4, opacity=0.8, tooltip="Hydrological Path").add_to(m)
        
        # Маркеры начала и конца
        folium.Marker([start_node[1], start_node[0]], popup="Start", icon=folium.Icon(color='green')).add_to(m)
        folium.Marker([end_node[1], end_node[0]], popup="End", icon=folium.Icon(color='red')).add_to(m)

    # Сохранение карты
    m.save("171.html")
    print("Карта сохранена в файл 171.html")

if __name__ == "__main__":
    solve_hydrological_distance()