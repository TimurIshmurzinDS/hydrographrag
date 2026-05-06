import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат (WKT) для демонстрации
coordinates = [
    {'name': 'Point1', 'geometry': wkt.loads('POINT(37.5 45.5)')},
    {'name': 'Point2', 'geometry': wkt.loads('POINT(38.0 46.0)')}
]

# Добавление точек на карту
for coord in coordinates:
    folium.Marker([coord['geometry'].y, coord['geometry'].x], popup=coord['name']).add_to(m)

# Сохранение карты
m.save("182.html")