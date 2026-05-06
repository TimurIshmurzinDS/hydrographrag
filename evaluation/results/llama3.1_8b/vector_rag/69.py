import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных из shapefile в GeoPandas DataFrame
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине области и использованием слоя CartoDB positron
m = folium.Map(location=basin_data.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление области на карту
folium.GeoJson(data=basin_data.to_json(), name='basin').add_to(m)

# Создание списка словарей для координат WKT (поскольку в контексте нет данных о конкретных координатах)
wkt_coords = [
    {'lat': 43.1234, 'lon': 76.5432},  # Примерные координаты
]

# Добавление маркеров на карту для каждой точки WKT
for coord in wkt_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сравнение текущего статуса датчиков на реке Koktal River и реке Aksu River (поскольку в контексте нет данных о статусе датчиков, мы не можем выполнить эту часть задачи)
print("Сравнение текущего статуса датчиков на реке Koktal River и реке Aksu River невозможно без доступа к данным о статусе датчиков.")

# Сохранение карты в файл
m.save("69.html")