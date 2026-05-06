import geopandas as gpd
import folium
from shapely import wkt
import networkx as nx

# Загрузка границы бассейна из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центре бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Приблизительные координаты созвездия Ориона и реки Шилик
orion_center = (35.1694, -80.8784)  # Примерные координаты центра созвездия Ориона
shilik_confluence = (35.2000, -80.9000)  # Примерные координаты точки соединения реки Шилик и Осек

# Добавление точек на карту
folium.Marker(orion_center, popup='Созвездие Ориона', icon=folium.Icon(color='red')).add_to(m)
folium.Marker(shilik_confluence, popup='Конфлюенция реки Шилик и Осек', icon=folium.Icon(color='blue')).add_to(m)

# Создание графа для нахождения кратчайшего пути
G = nx.Graph()
G.add_node('Orion', pos=orion_center)
G.add_node('ShilikConfluence', pos=shilik_confluence)

# Добавление ребра между узлами с весом (расстоянием)
distance = ((orion_center[0] - shilik_confluence[0])**2 + (orion_center[1] - shilik_confluence[1])**2)**0.5
G.add_edge('Orion', 'ShilikConfluence', weight=distance)

# Нахождение кратчайшего пути
shortest_path = nx.shortest_path(G, source='Orion', target='ShilikConfluence', weight='weight')

# Добавление пути на карту
for i in range(len(shortest_path) - 1):
    folium.PolyLine([shortest_path[i], shortest_path[i + 1]], color='purple').add_to(m)

# Сохранение карты
m.save("246.html")