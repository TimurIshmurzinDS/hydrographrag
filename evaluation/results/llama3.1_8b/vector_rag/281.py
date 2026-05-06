import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине области и использованием плиток CartoDB positron
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление области на карту
folium.GeoJson(basin_data.to_crs('EPSG:4326').geometry.__geo_interface__,
               name='Basin',
               style={'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если имеются координаты (WKT), создание hardcoded списка словарей
coordinates = [
    {'lat': 37.7749, 'lon': -122.4194},
    {'lat': 38.8977, 'lon': -77.0365}
]

# Добавление точек на карту
for coord in coordinates:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("281.html")