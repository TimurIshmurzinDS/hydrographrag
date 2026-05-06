import folium
import networkx as nx
from shapely.geometry import shape

# Загрузить данные о речных сетях в формате Shapefile (.shp)
river_network = shape('path/to/river_network.shp')

# Создать карту с помощью библиотеки Folium и добавить слой с данными о речной сети
m = folium.Map(location=[55.7558, 37.6173], zoom_start=10)
folium.GeoJson(river_network).add_child(folium.Marker(location=[55.7558, 37.6173])).add_to(m)

# Использовать алгоритм NetworkX для анализа иерархии речной сети
G = nx.DiGraph()
for feature in river_network['features']:
    G.add_edge(feature['properties']['source'], feature['properties']['sink'])

# Визуализировать результаты на карте с помощью библиотеки Folium
nx.draw(G, with_labels=True)
folium_static(m)

# Сохранить карту в файл
m.save("170.html")