import geopandas as gpd
from shapely.geometry import shape
import folium

# Сбор и подготовка данных о речной сети
river_network = gpd.read_file('river_network.shp')

# Создание сетки для моделирования потока воды
network_graph = river_network.copy()
network_graph['geometry'] = network_graph.apply(lambda row: shape(row.geometry), 1)

# Определение скорости течения воды в каждом участке реки
def calculate_flow_speed(row):
    # Примерная формула для расчета скорости течения
    return (row['length'] * row['width']) / (row['slope'] + 0.01)

network_graph['flow_speed'] = network_graph.apply(calculate_flow_speed, axis=1)

# Использование алгоритма для определения потенциальных путей распространения паводка
def flood_propagation(graph):
    # Примерная реализация алгоритма
    flooded_nodes = set()
    queue = [(graph.loc[0, 'geometry'], 0)]
    
    while queue:
        node, distance = queue.pop(0)
        
        if node not in flooded_nodes:
            flooded_nodes.add(node)
            
            for neighbor in graph.neighbors(node):
                queue.append((neighbor, distance + 1))
                
    return flooded_nodes

flooded_areas = flood_propagation(network_graph)

# Визуализация результатов на карте
m = folium.Map(location=[55.7558, 37.6173], zoom_start=10)
folium.GeoJson(flooded_areas.to_crs(epsg=3857).geometry.apply(lambda x: {'type': 'Feature', 'geometry': x}).tolist()).add_to(m)

# Сохранение карты в файл
m.save("179.html")