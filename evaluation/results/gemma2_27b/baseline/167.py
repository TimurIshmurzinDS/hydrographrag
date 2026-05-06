import geopandas as gpd
from shapely.geometry import LineString
from shapely.ops import transform
import pyproj

# Загрузка данных о речной сети
rivers = gpd.read_file("path/to/river_data.shp")

# Определение точек соединения рек Текес и Тентек
tekes_point = rivers[rivers["name"] == "Текес"].geometry.iloc[0]
tentek_point = rivers[rivers["name"] == "Тентек"].geometry.iloc[0]

# Создание линии моделирования
line = LineString([tekes_point, tentek_point])

# Расчет протяженности линии
length = line.length

print(f"Общая протяженность речной сети: {length} единиц измерения")

# Визуализация (необязательно)
import folium

m = folium.Map(location=[tekes_point.y, tekes_point.x], zoom_start=10)
folium.GeoJson(rivers).add_to(m)
folium.GeoJson(LineString([tekes_point, tentek_point]), color="red").add_to(m)

m.save("167.html")