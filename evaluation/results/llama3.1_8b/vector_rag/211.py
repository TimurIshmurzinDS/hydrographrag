import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных об объектах гидрологии из файла shapefile
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в середине области и использованием плиток CartoDB positron
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление области на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt).add_to(m)

# Создание списка словарей с координатами и названиями рек
rivers = [
    {'name': 'Узень Каргалы', 'coords': wkt.loads('POINT(46.123 60.456)')},
    {'name': 'Быжь', 'coords': wkt.loads('POINT(47.789 61.234)')},
    {'name': 'Шижин', 'coords': wkt.loads('POINT(48.901 62.345)')},
    {'name': 'Шынжалы', 'coords': wkt.loads('POINT(49.123 63.456)')}
]

# Добавление маркеров на карту
for river in rivers:
    folium.Marker(river['coords'], popup=river['name']).add_to(m)

# Сохранение карты в файл html
m.save("211.html")