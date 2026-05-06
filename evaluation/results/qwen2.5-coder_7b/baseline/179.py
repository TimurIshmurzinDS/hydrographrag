import geopandas as gpd
from shapely.geometry import LineString
import folium

# Загрузка данных о речных ветвях (пример данных)
data = {
    'geometry': [
        LineString([(0, 0), (1, 1)]),
        LineString([(1, 1), (2, 0)]),
        LineString([(2, 0), (3, 1)]),
        LineString([(3, 1), (4, 0)])
    ]
}

# Создание GeoDataFrame
gdf = gpd.GeoDataFrame(data)

# Определение направления потока воды для каждой ветви
def determine_flow_direction(line):
    if line.coords[0][0] < line.coords[-1][0]:
        return 'right'
    elif line.coords[0][0] > line.coords[-1][0]:
        return 'left'
    else:
        return 'up'

gdf['flow_direction'] = gdf.geometry.apply(determine_flow_direction)

# Симуляция распространения паводка
def simulate_flood_spread(gdf, start_node):
    flood_path = [start_node]
    current_node = start_node
    
    while True:
        next_nodes = []
        for i in range(len(gdf)):
            if gdf.iloc[i]['geometry'].coords[0] == current_node or gdf.iloc[i]['geometry'].coords[-1] == current_node:
                next_nodes.append(i)
        
        if not next_nodes:
            break
        
        # Выбор следующего узла (просто выбираем первый для примера)
        next_node = next_nodes[0]
        
        flood_path.append(gdf.iloc[next_node]['geometry'].coords[0] if gdf.iloc[next_node]['flow_direction'] == 'right' else gdf.iloc[next_node]['geometry'].coords[-1])
        current_node = flood_path[-1]
    
    return flood_path

# Начальный узел (например, первый узел)
start_node = gdf.geometry[0].coords[0]

# Симуляция распространения паводка
flood_path = simulate_flood_spread(gdf, start_node)

# Визуализация на карте
m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=10)

for i in range(len(flood_path) - 1):
    folium.PolyLine([flood_path[i], flood_path[i + 1]], color='red', weight=2.5, opacity=1).add_to(m)

m.save("179.html")