import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создать карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(data=basin_data.to_json(), name='Batareyka River Basin',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создать список словарей с координатами (WKT)
wkt_coords = [
    {"lat": 43.1234, "lon": 79.5678},
    {"lat": 43.2345, "lon": 80.6789}
]

# Добавить точки на карту
for coord in wkt_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], popup='Пиковый уровень воды').add_to(m)

# Сохранить карту в файл
m.save("49.html")