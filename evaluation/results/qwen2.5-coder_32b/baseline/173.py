import geopandas as gpd
from shapely.geometry import LineString
import networkx as nx
import folium

# Загрузка данных о реках (примерный путь к файлам)
rivers_gdf = gpd.read_file('path_to_rivers.shp')

# Фильтрация данных для получения только реки Шынжалы и основных речных систем
shynzhalys = rivers_gdf[rivers_gdf['name'] == 'Шынжалы']
main_river_systems = rivers_gdf[rivers_gdf['type'] == 'основная']

# Создание графа для топологической сети рек
G = nx.DiGraph()

for idx, row in rivers_gdf.iterrows():
    line = row.geometry
    coords = list(line.coords)
    for i in range(len(coords) - 1):
        G.add_edge(coords[i], coords[i + 1])

# Определение направления стока от реки Шынжалы к основным речным системам
def find_outlet(river_line, main_rivers_gdf):
    outlet = None
    for idx, row in main_rivers_gdf.iterrows():
        if river_line.intersects(row.geometry):
            intersection_point = river_line.intersection(row.geometry)
            if isinstance(intersection_point, LineString):
                outlet = intersection_point.coords[0]
            else:
                outlet = intersection_point.coords
            break
    return outlet

shynzhalys_outlet = find_outlet(shynzhalys.iloc[0].geometry, main_river_systems)

# Визуализация на карте с использованием folium
m = folium.Map(location=[42.8746, 74.5913], zoom_start=10)  # Примерные координаты Бишкека

# Добавление рек на карту
for idx, row in rivers_gdf.iterrows():
    points = list(row.geometry.coords)
    folium.PolyLine(points, color="blue", weight=2.5, opacity=1).add_to(m)

# Выделение реки Шынжалы и направления стока
shynzhalys_points = list(shynzhalys.iloc[0].geometry.coords)
folium.PolyLine(shynzhalys_points, color="red", weight=3.5, opacity=1).add_to(m)

# Добавление маркера для точки слияния реки Шынжалы с основной речью
if shynzhalys_outlet:
    folium.Marker(location=[shynzhalys_outlet[0][1], shynzhalys_outlet[0][0]], popup='Точка стока Шынжалы', icon=folium.Icon(color='green')).add_to(m)

# Сохранение карты в файл
m.save("173.html")