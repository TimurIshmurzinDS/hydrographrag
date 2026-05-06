import geopandas as gpd
from shapely.geometry import Point, LineString
import folium

# Шаг 1: Получение данных
# Предположим, что у нас есть GeoDataFrame с данными о водной сети реки Талгар.
# Для примера создадим искусственные данные.

# Создание линий (притоков и основного русла)
lines = [
    LineString([(10, 20), (15, 25)]),
    LineString([(15, 25), (20, 30)]),
    LineString([(15, 25), (25, 25)]),
    LineString([(25, 25), (30, 30)])
]

# Создание GeoDataFrame
gdf = gpd.GeoDataFrame(geometry=lines)

# Шаг 2: Подготовка данных
# Преобразуем линии в точки для определения узлов слияния

points = []
for line in gdf.geometry:
    points.extend(line.coords[:-1])  # Исключаем последнюю точку, чтобы избежать дублирования

point_gdf = gpd.GeoDataFrame(geometry=[Point(p) for p in points])

# Определяем узлы слияния как точки, которые встречаются более одного раза
node_counts = point_gdf.groupby(point_gdf.geometry).size()
nodes = node_counts[node_counts > 1].index

# Создаем GeoDataFrame для узлов слияния
nodes_gdf = gpd.GeoDataFrame(geometry=list(nodes))

# Шаг 3: Анализ структуры водной сети
# Узлы слияния уже определены в предыдущем шаге.

# Шаг 4: Визуализация результатов
# Создаем карту с использованием folium

m = folium.Map(location=[25, 25], zoom_start=10)

# Добавляем линии на карту
for _, row in gdf.iterrows():
    folium.PolyLine(locations=row.geometry.coords, color='blue').add_to(m)

# Добавляем узлы слияния на карту
for _, row in nodes_gdf.iterrows():
    folium.Marker(location=[row.geometry.y, row.geometry.x], popup="Узел слияния", icon=folium.Icon(color='red')).add_to(m)

# Сохраняем карту в файл
m.save("166.html")