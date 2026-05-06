import geopandas as gpd
from networkx import Graph, from_edgelist, is_connected
import folium

# Загрузка данных о речной сети реки Сарыкан (пример файла shapefile)
gdf = gpd.read_file('path_to_your_shapefile.shp')

# Создание графа из данных
G = Graph()

for index, row in gdf.iterrows():
    G.add_edge(row['start_node'], row['end_node'], weight=row['length'])

# Проверка связности графа
if is_connected(G):
    connectivity_coefficient = 1.0
else:
    connectivity_coefficient = 0.0

print(f"Коэффициент связности речной сети реки Сарыкан: {connectivity_coefficient}")

# Визуализация графа на карте
m = folium.Map(location=[gdf['y'].mean(), gdf['x'].mean()], zoom_start=10)

for index, row in gdf.iterrows():
    folium.PolyLine(
        locations=[[row['start_y'], row['start_x']], [row['end_y'], row['end_x']]],
        color='blue',
        weight=2,
        opacity=0.7
    ).add_to(m)

# Сохранение карты
m.save("175.html")