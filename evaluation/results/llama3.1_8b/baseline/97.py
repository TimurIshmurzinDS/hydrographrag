import geopandas as gpd
import networkx as nx
from folium import Map, Marker

# Загрузите данные о реках в формате GeoJSON или Shapefile.
gdf = gpd.read_file('path_to_your_data.shp')

# Создайте граф на основе данных о реках.
G = nx.Graph()
for index, row in gdf.iterrows():
    G.add_node(row['name'])
    for other_index, other_row in gdf.iterrows():
        if row['name'] != other_row['name']:
            intersection = gpd.overlay(row.geometry, other_row.geometry, how='intersection')
            if not intersection.empty:
                G.add_edge(row['name'], other_row['name'])

# Определите притоки реки Каратал.
karatal_neighbors = list(G.neighbors('Каратал'))

# Найдите длину участка, который образует река Емель.
emelya_length = 0
for neighbor in karatal_neighbors:
    if gdf.loc[gdf['name'] == neighbor, 'geometry'].iloc[0].length > emelya_length:
        emelya_length = gdf.loc[gdf['name'] == neighbor, 'geometry'].iloc[0].length

# Создайте визуализацию на карте с помощью библиотеки folium.
m = Map(location=[45.0, 75.0], zoom_start=10)
Marker(location=[45.0, 75.0]).add_to(m)

# Добавьте маркеры для рек Каратал и Емель.
for index, row in gdf.iterrows():
    if row['name'] == 'Каратал' or row['name'] == 'Емель':
        Marker(location=row.geometry.centroid).add_to(m)

# Сохраните карту в файл.
m.save("97.html")

print(f"Длина участка реки Емель, образующего приток реки Каратал: {emelya_length} метров.")