import folium
from geopandas import GeoDataFrame, read_file
from shapely.geometry import LineString
from networkx import Graph, shortest_path, dijkstra_path_length

# Загрузка данных о реках и промежуточных звеньях
shyzyn = read_file("path_to_shyzyn.shp")
dos = read_file("path_to_dos.shp")
intermediate_segments = read_file("path_to_intermediate_segments.shp")

# Создание графа
G = Graph()

# Добавление узлов (точек на пути)
for point in shyzyn.geometry:
    G.add_node(point.wkt)

for point in dos.geometry:
    G.add_node(point.wkt)

for segment in intermediate_segments.geometry:
    G.add_node(segment.centroid.wkt)

# Добавление ребер (отрезков между узлами)
for segment in intermediate_segments.geometry:
    start_point = segment.start_point.wkt
    end_point = segment.end_point.wkt
    G.add_edge(start_point, end_point, weight=segment.length)

# Поиск кратчайшего пути от Шыжын до Дос
shyzyn_centroid = shyzyn.geometry[0].centroid.wkt
dos_centroid = dos.geometry[0].centroid.wkt

shortest_path_nodes = shortest_path(G, source=shyzyn_centroid, target=dos_centroid)

# Расчет длины пути
total_length = dijkstra_path_length(G, source=shyzyn_centroid, target=dos_centroid, weight='weight')

print(f"Общая длина речного пути от Шыжын до Дос: {total_length} м")

# Визуализация на карте
m = folium.Map(location=[shyzyn.geometry[0].centroid.y, shyzyn.geometry[0].centroid.x], zoom_start=12)

folium.Marker([shyzyn.geometry[0].centroid.y, shyzyn.geometry[0].centroid.x], popup='Шыжын', icon=folium.Icon(color='red')).add_to(m)
folium.Marker([dos.geometry[0].centroid.y, dos.geometry[0].centroid.x], popup='Дос', icon=folium.Icon(color='blue')).add_to(m)

for segment in intermediate_segments.geometry:
    folium.PolyLine([(segment.xy[1][i], segment.xy[0][i]) for i in range(len(segment.xy[0]))], color='green').add_to(m)

m.save("100.html")