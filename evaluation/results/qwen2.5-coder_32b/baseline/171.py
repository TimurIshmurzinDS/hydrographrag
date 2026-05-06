import geopandas as gpd
from shapely.geometry import Point, LineString
import networkx as nx
import folium

# Загрузка данных о водных объектах из OpenStreetMap (примерный код для загрузки)
# В реальном проекте данные могут быть загружены с помощью osmnx или других библиотек
# Для примера используем готовые GeoDataFrame с реками и точками слияния

# Пример данных (замените на реальные данные из OSM)
data = {
    'name': ['Киши-Осек', 'Талгар'],
    'geometry': [Point(76.95, 43.21), Point(76.89, 43.18)]
}
points_gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

# Пример данных о реках (замените на реальные данные из OSM)
river_data = {
    'name': ['Киши-Осек', 'Талгар'],
    'geometry': [LineString([(76.95, 43.21), (76.90, 43.20)]),
                 LineString([(76.89, 43.18), (76.85, 43.17)])]
}
rivers_gdf = gpd.GeoDataFrame(river_data, crs="EPSG:4326")

# Построение графа
G = nx.Graph()

# Добавление ребер из данных о реках
for idx, row in rivers_gdf.iterrows():
    coords = list(row['geometry'].coords)
    for i in range(len(coords) - 1):
        G.add_edge(coords[i], coords[i + 1], weight=row['geometry'].length)

# Найти ближайшие точки на реках к точкам слияния
def find_nearest_point_on_line(point, line):
    nearest = min(line.coords, key=lambda coord: Point(coord).distance(point))
    return nearest

nearest_points = []
for point in points_gdf.geometry:
    nearest_point = None
    min_distance = float('inf')
    for river in rivers_gdf.geometry:
        nearest = find_nearest_point_on_line(point, river)
        distance = Point(nearest).distance(point)
        if distance < min_distance:
            min_distance = distance
            nearest_point = nearest
    nearest_points.append(nearest_point)

# Добавление точек слияния в граф и соединение их с ближайшими точками на реках
for i, point in enumerate(nearest_points):
    G.add_edge(tuple(point), tuple(points_gdf.geometry.iloc[i]), weight=Point(point).distance(points_gdf.geometry.iloc[i]))

# Вычисление гидрологического расстояния между точками слияния
start_point = nearest_points[0]
end_point = nearest_points[1]
shortest_path = nx.shortest_path(G, source=tuple(start_point), target=tuple(end_point), weight='weight')
hydrological_distance = sum(G.edges[u, v]['weight'] for u, v in zip(shortest_path[:-1], shortest_path[1:]))

print(f"Гидрологическое расстояние между точками слияния реки Киши-Осек и реки Талгар: {hydrological_distance} метров")

# Визуализация на карте
m = folium.Map(location=[43.20, 76.92], zoom_start=12)

# Добавление точек слияния
for point in points_gdf.geometry:
    folium.Marker([point.y, point.x]).add_to(m)

# Добавление рек
for river in rivers_gdf.geometry:
    folium.PolyLine([(p.y, p.x) for p in river.coords], color="blue").add_to(m)

# Добавление кратчайшего пути
folium.PolyLine([(p[1], p[0]) for p in shortest_path], color="red", weight=3).add_to(m)

m.save("171.html")