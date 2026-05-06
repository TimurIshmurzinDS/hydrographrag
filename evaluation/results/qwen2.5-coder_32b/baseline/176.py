import geopandas as gpd
from shapely.geometry import Point
import folium

# Шаг 1: Загрузка данных
# Предположим, что у нас есть два файла GeoJSON: 'terisbutak.geojson' и 'talgat.geojson'
terisbutak = gpd.read_file('terisbutak.geojson')
talgat = gpd.read_file('talgat.geojson')

# Шаг 2: Вычисление минимального расстояния
# Приведем данные к одной системе координат, если это необходимо
terisbutak = terisbutak.to_crs(epsg=4326)
talgat = talgat.to_crs(epsg=4326)

# Вычислим минимальное расстояние между линиями русла Терисбутак и реки Талгар
min_distance = float('inf')
closest_point_on_talgat = None
closest_point_on_terisbutak = None

for geom1 in terisbutak.geometry:
    for geom2 in talgat.geometry:
        distance = geom1.distance(geom2)
        if distance < min_distance:
            min_distance = distance
            closest_point_on_talgat = geom2.interpolate(geom2.project(geom1))
            closest_point_on_terisbutak = geom1.interpolate(geom1.project(geom2))

# Шаг 3: Визуализация результатов на карте с помощью folium
# Создадим карту, центрированную по средней точке между найденными ближайшими точками
center_lat = (closest_point_on_talgat.y + closest_point_on_terisbutak.y) / 2
center_lon = (closest_point_on_talgat.x + closest_point_on_terisbutak.x) / 2

m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

# Добавим линии русла Терисбутак и реки Талгар на карту
folium.GeoJson(terisbutak).add_to(m)
folium.GeoJson(talgat).add_to(m)

# Добавим точки минимального расстояния
folium.Marker(
    location=[closest_point_on_talgat.y, closest_point_on_talgat.x],
    popup='Ближайшая точка на реке Талгар',
    icon=folium.Icon(color='blue')
).add_to(m)

folium.Marker(
    location=[closest_point_on_terisbutak.y, closest_point_on_terisbutak.x],
    popup='Ближайшая точка на русле ручья Терисбутак',
    icon=folium.Icon(color='red')
).add_to(m)

# Добавим линию между ближайшими точками
line = folium.PolyLine(
    locations=[[closest_point_on_talgat.y, closest_point_on_talgat.x], [closest_point_on_terisbutak.y, closest_point_on_terisbutak.x]],
    color='green',
    weight=2.5,
    opacity=1
).add_to(m)

# Шаг 4: Сохранение карты в файл
m.save("176.html")