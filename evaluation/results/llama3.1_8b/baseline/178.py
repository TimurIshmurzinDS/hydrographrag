import geopandas as gpd
from shapely.geometry import Point
import folium

# Подготовка данных
gdf = gpd.read_file('path_to_your_shapefile.shp')

# Создание модели графов
import networkx as nx
G = nx.Graph()

# Добавление вершин и ребер в модель
for index, row in gdf.iterrows():
    G.add_node(row['name'], geometry=row.geometry)
    
for index, row in gdf.iterrows():
    for other_index, other_row in gdf.iterrows():
        if row['name'] != other_row['name']:
            intersection = row.geometry.intersection(other_row.geometry)
            if not intersection.is_empty:
                G.add_edge(row['name'], other_row['name'])

# Анализ топологии
from networkx.algorithms import community

communities = community.greedy_modularity_communities(G)

# Визуализация результатов
m = folium.Map(location=[55.7558, 37.6173], zoom_start=10)
for index, row in gdf.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup=row['name']).add_to(m)
    
for community in communities:
    for node in community:
        folium.CircleMarker([G.nodes[node]['geometry'].y, G.nodes[node]['geometry'].x],
                            radius=5,
                            color='red',
                            fill=True).add_to(m)

m.save("178.html")