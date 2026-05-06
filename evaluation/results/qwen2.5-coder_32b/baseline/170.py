import geopandas as gpd
import networkx as nx
from shapely.geometry import Point, LineString
import folium

# Загрузка данных о водных объектах (примерный путь к файлу)
water_network = gpd.read_file('path_to_water_network.shp')

# Предположим, что у нас есть поле 'type' для определения типа водного объекта
# и поле 'name' для названия ручья

# Идентификация начальной точки (ручья Терисбутак)
start_point = water_network[water_network['name'] == 'Терисбутак'].geometry.iloc[0]

# Создание графа
G = nx.DiGraph()

# Добавление ребер в граф
for i, row in water_network.iterrows():
    if row.geometry.type == 'LineString':
        start_node = (row.geometry.coords[0][0], row.geometry.coords[0][1])
        end_node = (row.geometry.coords[-1][0], row.geometry.coords[-1][1])
        G.add_edge(start_node, end_node, geometry=row.geometry)

# Поиск пути от начальной точки до основных артерий
def find_main_arteries(G, start_point):
    main_arteries = []
    for node in G.nodes:
        if len(list(G.successors(node))) == 0:  # Предполагаем, что конечные узлы - это основные артерии
            path = nx.shortest_path(G, source=start_point, target=node)
            main_arteries.append(path)
    return main_arteries

main_arteries_paths = find_main_arteries(G, start_point)

# Визуализация на карте с использованием folium
m = folium.Map(location=[start_point.y, start_point.x], zoom_start=12)

# Добавление ручья Терисбутак на карту
folium.Marker([start_point.y, start_point.x], popup='Терисбутак', icon=folium.Icon(color='green')).add_to(m)

# Добавление основных артерий на карту
for path in main_arteries_paths:
    folium.PolyLine([(G.nodes[node]['y'], G.nodes[node]['x']) for node in path], color="blue", weight=2.5, opacity=1).add_to(m)

# Сохранение карты в файл
m.save("170.html")