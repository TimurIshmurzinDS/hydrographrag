import geopandas as gpd
from shapely.geometry import Point
from shapely.topology import intersects
from geopy.distance import geodesic

# Загрузить данные о реках
rivers = gpd.read_file("rivers.shp")

# Найти реки по имени
shyzhyny = rivers[rivers["name"] == "Шыжын"].iloc[0]
dos = rivers[rivers["name"] == "Дос"].iloc[0]

# Проверить, является ли Шыжын притоком Доса
if intersects(Point(shyzhyny.geometry.coords[0]), dos.geometry):
    print("Река Шыжын является притоком реки Дос.")
else:
    print("Река Шыжын не является притоком реки Дос.")

# Вычислить расстояние до слияния
merge_point = shyzhyny.geometry.coords[-1]
distance = geodesic(shyzhyny.geometry.coords[0], merge_point)

print("Расстояние до слияния:", distance)

# Визуализировать результат на карте
import folium

m = folium.Map(location=[shyzhyny.geometry.coords[0][1], shyzhyny.geometry.coords[0][0]], zoom_start=12)

folium.GeoJson(rivers[rivers["name"] == "Шыжын"], name="Шыжын").add_to(m)
folium.GeoJson(rivers[rivers["name"] == "Дос"], name="Дос").add_to(m)

folium.Marker(location=merge_point, popup="Слияние").add_to(m)

m.save("104.html")