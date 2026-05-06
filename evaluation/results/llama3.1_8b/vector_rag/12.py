import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне в формате shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=basin_data.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(data=basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей для координат (WKT)
wkt_coords = [
    {"lat": 55.123456, "lon": 37.654321},
    {"lat": 55.234567, "lon": 38.765432}
]

# Добавление точек на карту
for coord in wkt_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("12.html")