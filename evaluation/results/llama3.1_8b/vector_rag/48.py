import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в координатах центра shapefile и параметрами tiles='CartoDB positron'
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту с использованием folium.GeoJson
folium.GeoJson(data=basin_data.to_json(), name='basin').add_to(m)

# Создание списка словарей для координат (WKT)
wkt_coords = [
    {'lat': 43.1234, 'lon': 77.5678},
    {'lat': 42.9012, 'lon': 78.3456}
]

# Добавление маркеров на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл с именем "48.html"
m.save("48.html")