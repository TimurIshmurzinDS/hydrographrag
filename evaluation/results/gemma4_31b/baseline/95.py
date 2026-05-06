import osmnx as ox
import networkx as nx
import folium
from shapely.geometry import LineString, Point

def solve_river_connectivity():
    # 1. Определяем область поиска (район Алматы и горы)
    place_name = "Almaty, Kazakhstan"
    
    print("Загрузка гидрографических данных из OSM...")
    # Извлекаем все объекты с тегом waterway
    gdf = ox.features_from_place(place_name, tags={"waterway": True})
    
    # Фильтруем только линейные объекты (реки)
    rivers = gdf[gdf.geometry.type == 'LineString']
    
    # 2. Поиск целевых рек по именам
    # Примечание: в OSM названия могут быть на разных языках или с вариациями
    target_1 = "Улькен Алматы" # Большой Алматы
    target_2 = "Шыжын"
    
    # Поиск всех сегментов, относящихся к этим рекам
    river_1_segments = rivers[rivers['name'].str.contains(target_1, na=False, case=False)]
    river_2_segments = rivers[rivers['name'].str.contains(target_2, na=False, case=False)]
    
    if river_1_segments.empty or river_2_segments.empty:
        print(f"Одна из рек не найдена в базе OSM. Проверка по альтернативным именам...")
        # Попробуем найти по английским/другим названиям, если основные не найдены
        river_1_segments = rivers[rivers['name'].str.contains("Bolshoy Almaty", na=False, case=False)]
        river_2_segments = rivers[rivers['name'].str.contains("Shyzyn", na=False, case=False)]

    # 3. Построение графа связности
    G = nx.Graph()
    
    for idx, row in rivers.iterrows():
        coords = list(row.geometry.coords)
        for i in range(len(coords) - 1):
            u = coords[i]
            v = coords[i+1]
            # Добавляем ребро с атрибутом имени реки
            G.add_edge(u, v, name=row.get('name', 'unknown'))

    # Определяем узлы, принадлежащие нашим рекам
    nodes_r1 = set()
    for geom in river_1_segments.geometry:
        nodes_r1.update(geom.coords)
        
    nodes_r2 = set()
    for geom in river_2_segments.geometry:
        nodes_r2.update(geom.coords)

    # 4. Проверка связности
    connected = False
    path = []
    
    if nodes_r1 and nodes_r2:
        # Проверяем наличие пути между любым узлом первой реки и любым узлом второй
        # Для оптимизации берем один репрезентативный узел от каждой
        start_node = list(nodes_r1)[0]
        end_node = list(nodes_r2)[0]
        
        try:
            path = nx.shortest_path(G, source=start_node, target=end_node)
            connected = True
        except nx.NetworkXNoPath:
            connected = False

    # 5. Визуализация
    print(f"Связность: {'Обнаружена' if connected else 'Не обнаружена'}")
    
    # Создаем карту, центрированную по одной из рек
    center_lat = river_1_segments.geometry.centroid.y.mean() if not river_1_segments.empty else 43.2
    center_lon = river_1_segments.geometry.centroid.x.mean() if not river_1_segments.empty else 76.9
    m = folium.Map(location=[center_lat, center_lon], zoom_start=11, tiles='CartoDB positron')

    # Отрисовка всех рек (серым)
    for _, row in rivers.iterrows():
        coords = [[p[1], p[0]] for p in row.geometry.coords]
        folium.PolyLine(coords, color="blue", weight=1, opacity=0.3).add_to(m)

    # Отрисовка Реки 1 (Красный)
    for _, row in river_1_segments.iterrows():
        coords = [[p[1], p[0]] for p in row.geometry.coords]
        folium.PolyLine(coords, color="red", weight=3, opacity=0.8, tooltip=target_1).add_to(m)

    # Отрисовка Реки 2 (Зеленый)
    for _, row in river_2_segments.iterrows():
        coords = [[p[1], p[0]] for p in row.geometry.coords]
        folium.PolyLine(coords, color="green", weight=3, opacity=0.8, tooltip=target_2).add_to(m)

    # Отрисовка пути, если он найден (Желтый)
    if connected:
        path_coords = [[p[1], p[0]] for p in path]
        folium.PolyLine(path_coords, color="yellow", weight=5, opacity=0.9, tooltip="Путь связи").add_to(m)

    # Сохранение карты
    m.save("95.html")
    print("Результат сохранен в файл 95.html")

if __name__ == "__main__":
    solve_river_connectivity()