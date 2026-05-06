import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне в формате shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в координатах центра бассейна и использованием слоя CartoDB positron
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление данных о бассейне на карту в виде GeoJson с зеленой заливкой и прозрачностью 20%
folium.GeoJson(basin_data.to_crs(epsg=4326).geometry.apply(lambda x: x.wkt)).add_to(m)

# Создание списка словарей для координат (WKT)
wkt_coordinates = [
    {'lat': 55.123, 'lon': 37.456},
    {'lat': 55.789, 'lon': 38.901}
]

# Добавление маркеров на карту по координатам
for coord in wkt_coordinates:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл с именем "34.html"
m.save("34.html")