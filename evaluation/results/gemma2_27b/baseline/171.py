import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузка данных о реках
rivers = gpd.read_file("path/to/river/data.shp")

# Определение точек слияния (замените на реальные координаты)
merge_point = Point(47.12345, 82.65432)

# Расчет гидрологического расстояния (замените на подходящий алгоритм)
hydrological_distance = rivers.distance(Point(merge_point))

# Создание карты с помощью folium
m = folium.Map(location=[47.12345, 82.65432], zoom_start=10)

# Добавление рек на карту
folium.GeoJson("path/to/river/data.shp").add_to(m)

# Добавление точки слияния на карту
folium.Marker(location=[merge_point.y, merge_point.x], popup="Точка слияния").add_to(m)

# Сохранение карты
m.save("171.html")