import geopandas as gpd
from shapely.geometry import Point
import networkx as nx
import folium

# Загрузим данные о местоположении датчиков и точках измерения.
sensors_gdf = gpd.read_file('sensors.shp')
measurements_gdf = gpd.read_file('measurements.shp')

# Создадим слой для каждого из двух рек, используя их геометрии.
river1_gdf = gpd.read_file('river1.shp')
river2_gdf = gpd.read_file('river2.shp')

# Добавим точки измерения к слоям рек.
river1_gdf['measurements'] = measurements_gdf[measurements_gdf['river_name'] == 'Токыраун']
river2_gdf['measurements'] = measurements_gdf[measurements_gdf['river_name'] == 'Аягоз']

# Создадим сети для каждой реки.
G1 = nx.Graph()
G2 = nx.Graph()

for index, row in river1_gdf.iterrows():
    for measurement in row['measurements']:
        G1.add_node(measurement['id'])
        G1.add_edge(measurement['id'], row['id'])

for index, row in river2_gdf.iterrows():
    for measurement in row['measurements']:
        G2.add_node(measurement['id'])
        G2.add_edge(measurement['id'], row['id'])

# Оценим стабильность связи на каждой реке.
stability1 = nx.average_shortest_path_length(G1)
stability2 = nx.average_shortest_path_length(G2)

print(f'Стабильность связи на реке Токыраун: {stability1}')
print(f'Стабильность связи на реке Аягоз: {stability2}')

# Визуализируем результаты на карте.
m = folium.Map(location=[46.5, 73.0], zoom_start=10)

folium.Marker([river1_gdf.geometry.y.mean(), river1_gdf.geometry.x.mean()], popup='Токыраун').add_to(m)
folium.Marker([river2_gdf.geometry.y.mean(), river2_gdf.geometry.x.mean()], popup='Аягоз').add_to(m)

m.save("140.html")