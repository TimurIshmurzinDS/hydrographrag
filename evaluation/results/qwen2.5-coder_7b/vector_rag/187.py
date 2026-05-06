import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границей бассина
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассина на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат WKT (если они есть)
coordinates = [
    {'name': 'Farm1', 'geometry': wkt.loads('POINT(37.422 -122.084)')},
    {'name': 'Farm2', 'geometry': wkt.loads('POINT(37.425 -122.086)')}
]

# Добавление ферм на карту
for coord in coordinates:
    folium.Marker([coord['geometry'].y, coord['geometry'].x], popup=coord['name']).add_to(m)

# Сохранение карты
m.save("187.html")