import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границы бассейна из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре границы бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Координаты наблюдательных пунктов (пример)
observation_points = [
    {'name': 'Point1', 'wkt': 'POINT(43.5678 40.1234)'},
    {'name': 'Point2', 'wkt': 'POINT(43.5789 40.2345)'},
    {'name': 'Point3', 'wkt': 'POINT(43.5890 40.3456)'}
]

# Преобразование WKT в объекты Shapely
observation_points = [{'name': point['name'], 'geometry': wkt.loads(point['wkt'])} for point in observation_points]

# Добавление наблюдательных пунктов на карту
for point in observation_points:
    folium.Marker([point['geometry'].y, point['geometry'].x], popup=point['name']).add_to(m)

# Сохранение карты в файл
m.save("78.html")