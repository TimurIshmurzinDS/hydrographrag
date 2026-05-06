import networkx as nx
import folium

# Create a graph with rivers as nodes and their tributaries as edges
G = nx.DiGraph()

# Add rivers to the graph
G.add_node("Тентек")
G.add_node("Быж")
G.add_node("Емель")

# Define tributaries (edges)
G.add_edge("Быж", "Емель")  # Быж is a tributary of Емель

# Find all upstream nodes (tributaries) of the river Емель
upstream_nodes = list(nx.upstream(G, "Емель"))

# Create a map using Folium
m = folium.Map(location=[50.4936, 86.9724], zoom_start=10)

# Add rivers to the map as polylines
for node in G.nodes:
    if node == "Емель":
        folium.PolyLine([[50.4936, 86.9724]], weight=5, color="blue").add_to(m)
    elif node in upstream_nodes:
        folium.PolyLine([[50.4936, 86.9724], [51.0, 87.0]], weight=3, color="green").add_to(m)
    else:
        folium.PolyLine([[50.4936, 86.9724], [51.5, 87.5]], weight=1, color="black").add_to(m)

# Save the map
m.save("101.html")