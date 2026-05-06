import networkx as nx
import folium

# Coordinates of Orion constellation and Shilka river
orion = (38.7167, -90.5333)
shilka_river = (52.2833, 124.7)

# Create a graph with two nodes: Orion and Shilka River
G = nx.Graph()
G.add_node("Orion", pos=orion)
G.add_node("Shilka River", pos=shilka_river)

# Calculate the shortest path between Orion and Shilka River
path = nx.shortest_path(G, "Orion", "Shilka River")

# Create a map centered at the midpoint of the path
midpoint = ((orion[0] + shilka_river[0]) / 2, (orion[1] + shilka_river[1]) / 2)
m = folium.Map(location=midpoint, zoom_start=4)

# Draw the shortest path on the map
for i in range(len(path) - 1):
    folium.PolyLine(locations=[G.nodes[path[i]]['pos'], G.nodes[path[i + 1]]['pos']]).add_to(m)

# Save the map as "246.html"
m.save("246.html")