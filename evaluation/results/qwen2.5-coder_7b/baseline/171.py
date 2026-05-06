import geopandas as gpd
from shapely.geometry import Point, LineString
import networkx as nx
import folium

# Загрузка геоданных о реках
kishi_osak = gpd.read_file('path_to_kishi_osak.shp')
talgar = gpd.read_file('path_to_talgar.shp')

# Создание графа
G = nx.Graph()

# Добавление узлов и ребер в граф
for idx, row in kishi_osak.iterrows():
    if isinstance(row['geometry'], LineString):
        for i in range(len(row['geometry'].coords) - 1):
            start_point = Point(row['geometry'].coords[i])
            end_point = Point(row['geometry'].coords[i + 1])
            G.add_edge(start_point, end_point)

for idx, row in talgar.iterrows():
    if isinstance(row['geometry'], LineString):
        for i in range(len(row['geometry'].coords) - 1):
            start_point = Point(row['geometry'].coords[i])
            end_point = Point(row['geometry'].coords[i + 1])
            G.add_edge(start_point, end_point)

# Нахождение точек слияния
merge_points_kishi_osak = kishi_osak[kishi_osak.duplicated(subset='geometry', keep=False)]
merge_points_talgar = talgar[talgar.duplicated(subset='geometry', keep=False)]

# Вычисление кратчайшего пути между точками слияния
start_point = merge_points_kishi_osak.iloc[0]['geometry']
end_point = merge_points_talgar.iloc[0]['geometry']

try:
    path = nx.shortest_path(G, source=start_point, target=end_point, weight='weight')
    distance = nx.shortest_path_length(G, source=start_point, target=end_point, weight='weight')
except nx.NetworkXNoPath:
    print("Путь между точками слияния не найден.")
else:
    print(f"Гидрологическое расстояние: {distance} м")

# Визуализация на карте
m = folium.Map(location=[(start_point.y + end_point.y) / 2, (start_point.x + end_point.x) / 2], zoom_start=10)

folium.Marker([start_point.y, start_point.x], popup='Начало', icon=folium.Icon(color='red')).add_to(m)
folium.Marker([end_point.y, end_point.x], popup='Конец', icon=folium.Icon(color='blue')).add_to(m)

for u, v in path:
    folium.PolyLine([(u.y, u.x), (v.y, v.x)], color='green').add_to(m)

m.save("171.html")