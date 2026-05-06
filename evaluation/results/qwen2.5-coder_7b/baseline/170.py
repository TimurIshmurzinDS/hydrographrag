import geopandas as gpd
from shapely.geometry import Point, LineString
import folium

# Загрузка данных о речных ветвях (пример: Shapefile)
gdf = gpd.read_file('path_to_your_shapefile.shp')

# Определение узлов и ребер
nodes = set()
edges = []

for index, row in gdf.iterrows():
    geometry = row.geometry
    if isinstance(geometry, LineString):
        for point in geometry.coords:
            nodes.add(Point(point))
        edges.append((row['id'], geometry))

# Сортировка по длине
sorted_edges = sorted(edges, key=lambda x: x[1].length, reverse=True)

# Построение дерева
tree = {}
for edge in sorted_edges:
    edge_id, line = edge
    start_point = line.coords[0]
    end_point = line.coords[-1]
    
    if start_point not in tree:
        tree[start_point] = []
    if end_point not in tree:
        tree[end_point] = []
    
    tree[start_point].append((edge_id, end_point))
    tree[end_point].append((edge_id, start_point))

# Визуализация на карте
m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=10)

for index, row in gdf.iterrows():
    geometry = row.geometry
    if isinstance(geometry, LineString):
        folium.PolyLine(locations=list(geometry.coords), color='blue', weight=2.5, opacity=1).add_to(m)

# Сохранение карты
m.save("170.html")