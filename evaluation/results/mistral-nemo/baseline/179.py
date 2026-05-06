import geopandas as gpd
from shapely.geometry import Point
import networkx as nx
import folium

# 1. Подготовьте данные о речной сети
river_network = gpd.read_file('rivers.shp')  # Замените на путь к вашим данным о речной сети

# 2. Идентифицируйте стартовую точку - реку Киши-Осек
start_river = 'Киши-Осек'  # Замените на название вашей реки
start_point = Point(river_network.loc[river_network['name'] == start_river].geometry.x, river_network.loc[river_network['name'] == start_river].geometry.y)

# 3. Используйте модель распространения паводка
G = nx.from_geopandas(river_network)
path = nx.dijkstra_path(G, source=start_point, target='end_point')  # Замените 'end_point' на конечную точку вашего анализа

# 4. Визуализируйте результаты моделирования на карте
m = folium.Map(location=[start_point.y, start_point.x], zoom_start=13)

folium.GeoJson(river_network[['geometry']]).add_to(m)
folium.PolyLine(locations=[(p.y, p.x) for p in path], weight=2.5).add_to(m)

# 5. Сохраните финальную карту в формате HTML
m.save("179.html")