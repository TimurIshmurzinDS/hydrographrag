import networkx as nx
import folium

# Загрузите данные о реках и их взаимосвязях
G = nx.read_gpickle('river_network.gpickle')

# Создайте топологию сети, представляющую связь между различными участками реки Шынжалы и основными речными системами.
river_shynzhaly = 'Шынжалы'
main_river_systems = ['Карауылколь', 'Алаколь']

# Добавьте ребра в топологию сети, представляющие связь между рекой Шынжалы и основными речными системами.
for river in main_river_systems:
    G.add_edge(river_shynzhaly, river)

# Рассчитайте направление стока для каждого участка реки Шынжалы на основе топологии сети.
flow_direction = nx.floyd_warshall(G)

# Проанализируйте результаты и представьте их в виде карты.
m = folium.Map(location=[46.5, 68.0], zoom_start=10)
folium.Marker([46.5, 68.0], popup='Река Шынжалы').add_to(m)

for river in G.nodes():
    if river != river_shynzhaly:
        flow = flow_direction[river_shynzhaly][river]['weight']
        folium.CircleMarker([G.nodes()[river]['lat'], G.nodes()[river]['lon']], radius=flow*10, color='blue').add_to(m)

m.save("173.html")