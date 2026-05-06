import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с внешними границами бассейна
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту с зеленой заливкой
folium.GeoJson(basin_gdf.to_json(), name='basin').add_to(m)

# Создание hardcoded списка словарей для координат (WKT)
wkt_coords = [
    {'lat': 43.1234, 'lon': 76.5432},
    {'lat': 43.2345, 'lon': 76.6543},
    {'lat': 43.3456, 'lon': 76.7654}
]

# Добавление координат на карту
for coord in wkt_coords:
    folium.CircleMarker(location=[coord['lat'], coord['lon']], radius=5).add_to(m)

# Сохранение карты в файл
m.save("229.html")