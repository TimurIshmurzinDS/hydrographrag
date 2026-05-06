import networkx as nx
from folium import Map, Polygon, Marker
import geopandas as gpd

# Загрузите данные о реках в формате GeoJSON.
river_data = gpd.read_file('path_to_your_river_data.shp')

# Создайте граф NetworkX и добавьте вершины (реки) и ребра (связь между реками).
G = nx.Graph()
for index, row in river_data.iterrows():
    G.add_node(row['name'])
    for other_index, other_row in river_data.iterrows():
        if row['name'] != other_row['name']:
            G.add_edge(row['name'], other_row['name'])

# Находите кратчайший путь между рекой Текес и рекой Тентек.
shortest_path = nx.shortest_path(G, source='Река Текес', target='Река Тентек')

# Рассчитайте общую протяженность речной сети.
total_length = 0
for i in range(len(shortest_path) - 1):
    total_length += G[shortest_path[i]][shortest_path[i + 1]]['length']

print(f'Общая протяженность речной сети: {total_length} единиц')

# Создайте карту с помощью библиотеки Folium.
m = Map(location=[river_data.centroid.y.mean(), river_data.centroid.x.mean()], zoom_start=10)
for index, row in river_data.iterrows():
    Polygon([(row['geometry'].bounds[0], row['geometry'].bounds[1]),
             (row['geometry'].bounds[0], row['geometry'].bounds[3]),
             (row['geometry'].bounds[2], row['geometry'].bounds[3]),
             (row['geometry'].bounds[2], row['geometry'].bounds[1])],
            color='blue', fill=True).add_to(m)
    Marker([row['geometry'].centroid.y, row['geometry'].centroid.x]).add_to(m)

# Сохраните карту в файл.
m.save("167.html")