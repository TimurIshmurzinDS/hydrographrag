import geopandas as gpd
from shapely.geometry import LineString
from shapely.ops import linemerge
import folium

# Загрузка данных о реках
rivers = gpd.read_file("rivers.shp")

# Выделение реки Эмель и Сарыкан
emil = rivers[rivers["name"] == "Эмель"]
sarykan = rivers[rivers["name"] == "Сарыкан"]

# Определение узлов и ребер (пример)
nodes = []
edges = []
for i in range(len(rivers)):
    line = rivers.geometry[i]
    if isinstance(line, LineString):
        edges.append(line)
        nodes.extend(line.coords)

# Анализ связности (пример с использованием поиска в глубину)
def dfs(graph, start, end):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node == end:
            return True
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)
    return False

# Создание графа связности (пример)
graph = {}
for edge in edges:
    start_node = edge.coords[0]
    end_node = edge.coords[-1]
    if start_node not in graph:
        graph[start_node] = []
    if end_node not in graph:
        graph[end_node] = []
    graph[start_node].append(end_node)
    graph[end_node].append(start_node)

# Проверка связности между реками
connected = dfs(graph, emil.geometry[0].coords[0], sarykan.geometry[0].coords[-1])

# Визуализация
m = folium.Map(location=[45.2, 63.3], zoom_start=8)
folium.GeoJson("rivers.shp").add_to(m)
if connected:
    folium.PolyLine(locations=[emil.geometry[0].coords[0], sarykan.geometry[0].coords[-1]], color="green").add_to(m)

m.save("168.html")