import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузка данных о притоках и точках слияния
prongs = gpd.read_file('path_to_prongs.shp')
confluences = gpd.read_file('path_to_confluences.shp')

# Создание графа
graph = {}
for _, row in prongs.iterrows():
    start_point = Point(row['geometry'].coords[0])
    end_point = Point(row['geometry'].coords[-1])
    
    if start_point not in graph:
        graph[start_point] = []
    if end_point not in graph:
        graph[end_point] = []
    
    graph[start_point].append(end_point)

# Поиск циклов
def dfs(node, visited, stack):
    visited.add(node)
    stack.append(node)
    
    for neighbor in graph[node]:
        if neighbor not in visited:
            if dfs(neighbor, visited, stack):
                return True
        elif neighbor in stack:
            return True
    
    stack.pop()
    return False

# Определение узлов слияния
confluence_nodes = set(confluences.geometry)
visited = set()

for node in confluence_nodes:
    if node not in visited:
        dfs(node, visited, [])

# Визуализация на карте
m = folium.Map(location=[confluences.geometry.centroid.y.mean(), confluences.geometry.centroid.x.mean()], zoom_start=10)

for _, row in confluences.iterrows():
    folium.Marker([row['geometry'].centroid.y, row['geometry'].centroid.x], popup=row['name'], icon=folium.Icon(color='red')).add_to(m)

for node in graph:
    if node in visited:
        folium.CircleMarker([node.y, node.x], radius=5, color='blue', fill=True, fill_color='blue').add_to(m)

m.save("166.html")