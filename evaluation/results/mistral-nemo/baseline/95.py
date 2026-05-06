import geopandas as gpd
from shapely.geometry import Point
import networkx as nx
import folium

# 1. Получение данных о реках
ulken_almaty = {'name': 'Улькен Алматы', 'geometry': Point(74.82, 43.25)}
shyzyn = {'name': 'Шыжын', 'geometry': Point(69.01, 43.56)}

rivers_gdf = gpd.GeoDataFrame([ulken_almaty, shyzyn], geometry='geometry')

# 2. Построение гидрографической сети
G = nx.DiGraph()

for idx, river in rivers_gdf.iterrows():
    G.add_node(river['name'], geometry=river['geometry'])

# Добавляем связи между реками (притоки)
# Для этого нам понадобятся данные о притоках, которые мы получим из внешнего источника
# Пример: если река А является притоком реки Б, то добавляем ребро (А, Б) в G

# 3. Анализ связей между реками
def is_connected(G, node1, node2):
    return nx.has_path(G, node1, node2)

if is_connected(G, 'Улькен Алматы', 'Шыжын'):
    print("Реки связаны через систему притоков.")
else:
    print("Реки не связаны через систему притоков.")

# Визуализация на карте (для демонстрации)
m = folium.Map(location=[43.25, 74.82], zoom_start=8)

for node in G.nodes():
    folium.Marker(G.nodes()[node]['geometry']).add_to(m)

m.save("95.html")