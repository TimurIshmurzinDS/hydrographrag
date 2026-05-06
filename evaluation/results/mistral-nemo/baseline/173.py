import geopandas as gpd
import networkx as nx
from shapely.geometry import Point
import folium

# 1. Подготовка данных
river_network = gpd.read_file("river_network.shp") # Замените на путь к вашим данным о речной сети
shynjaly_river = river_network[river_network['name'] == 'Шынжалы']

# 2. Анализ топологии сети
G = nx.from_geopandas(river_network)
connected_systems = list(nx.dfs_successors(G, shynjaly_river.geometry.iloc[0]).keys())

# 3. Определение направления стока
def get_flow_direction(geometry1, geometry2):
    p1 = Point(geometry1.x, geometry1.y)
    p2 = Point(geometry2.x, geometry2.y)
    if p1.distance(p2) > 0:
        return (p2 - p1).normalize()
    else:
        return None

flow_directions = {}
for system in connected_systems:
    flow_direction = get_flow_direction(shynjaly_river.geometry.iloc[0], river_network.loc[system, 'geometry'])
    if flow_direction is not None:
        flow_directions[system] = flow_direction

# 4. Визуализация результатов
m = folium.Map(location=[shynjaly_river.geometry.y.mean(), shynjaly_river.geometry.x.mean()], zoom_start=8)

folium.GeoJson(shynjaly_river.__geo_interface__).add_to(m)
for system, direction in flow_directions.items():
    system_geometry = river_network.loc[system, 'geometry']
    folium.PolyLine([(system_geometry.x, system_geometry.y), (shynjaly_river.geometry.x.iloc[0], shynjaly_river.geometry.y.iloc[0])], weight=2).add_to(m)

m.save("173.html")