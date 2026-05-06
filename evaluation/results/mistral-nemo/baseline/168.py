import geopandas as gpd
from shapely.ops import graph_from_features
from networkx.algorithms.shortest_paths.weighted import dijkstra_path
import folium

# Load river data and basin data
rivers = gpd.read_file("rivers.shp")
basins = gpd.read_file("basins.shp")

# Find the source of Emel River
emel_source = rivers[rivers['name'] == 'Emel'].iloc[0]

# Build flow graph using Shapely's graph_from_features function
graph = graph_from_features(rivers.geometry)

# Use Dijkstra's algorithm to find shortest path from Emel's source to its mouth
path = dijkstra_path(graph, emel_source, rivers[rivers['name'] == 'Emel'].iloc[-1])

# Find connected tributaries of Emel River
connected_tributaries = set()
for node in path:
    if rivers.loc[node, 'name'] != 'Emel':
        connected_tributaries.add(rivers.loc[node, 'name'])

# Print connected tributaries
print("Connected tributaries of Emel River:")
for trib in connected_tributaries:
    print(trib)

# Create a map using Folium
m = folium.Map(location=[basins.centroid.y.mean(), basins.centroid.x.mean()], zoom_start=8)

# Add rivers to the map
for _, row in rivers.iterrows():
    folium.GeoJson(row.geometry, style_function=lambda x: {'fillColor': 'blue'}).add_to(m)

# Save the map as HTML file
m.save("168.html")