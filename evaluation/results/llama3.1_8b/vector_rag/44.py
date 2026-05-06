import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными бассейна в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_data.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту с прозрачностью 20%
folium.GeoJson(basin_data.to_json(), name='Basin').add_to(m)

# Создание списка словарей для координат WKT (если они есть)
wkt_coords = [
    {'lat': 43.1234, 'lon': 77.5678},
    {'lat': 42.9012, 'lon': 78.3456}
]

# Добавление маркеров на карту для координат WKT
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл с именем '44.html'
m.save("44.html")