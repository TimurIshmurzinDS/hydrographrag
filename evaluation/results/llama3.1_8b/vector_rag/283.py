import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными бассейна
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в координатах центра бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту с fillOpacity=0.2
folium.GeoJson(basin_data.to_json(), name='basin').add_to(m)

# Создание списка словарей для координат (WKT)
wkt_coords = [
    {'lat': 55.7558, 'lon': 37.6173},
    {'lat': 40.7128, 'lon': -74.0060}
]

# Добавление маркеров на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], popup='Маркер').add_to(m)

# Сохранение карты в файл с именем "283.html"
m.save("283.html")