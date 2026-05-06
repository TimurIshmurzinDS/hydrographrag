import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import transform
import pyproj
import folium

# Загрузка данных о реках
rivers = gpd.read_file("path/to/river/data.geojson")

# Нахождение точек начала рек
urzar_source = rivers[rivers["name"] == "Уржар"].geometry.iloc[0].Point()
dos_source = rivers[rivers["name"] == "Дос"].geometry.iloc[0].Point()

# Расчет расстояния между точками
def calculate_distance(point1, point2):
    geod = pyproj.Geod(ellps='WGS84')
    return geod.inv(point1.x, point1.y, point2.x, point2.y)[2]

distance = calculate_distance(urzar_source, dos_source)

# Визуализация на карте
m = folium.Map(location=[45.0, 60.0], zoom_start=8)
folium.Marker(location=[urzar_source.y, urzar_source.x], popup="Уржар").add_to(m)
folium.Marker(location=[dos_source.y, dos_source.x], popup="Дос").add_to(m)

# Сохранение карты
m.save("96.html")

print(f"Расстояние между реками Уржар и Дос: {distance} метров")