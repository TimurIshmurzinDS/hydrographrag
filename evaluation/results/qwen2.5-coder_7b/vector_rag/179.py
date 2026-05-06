import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассина
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассина и использованием тайлов CartoDB positron
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границы бассина на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Создание списка координат наблюдаемых точек (WKT)
observation_points = [
    {'name': 'Point1', 'wkt': 'POINT(37.422 -122.084)'},
    {'name': 'Point2', 'wkt': 'POINT(37.425 -122.090)'},
    {'name': 'Point3', 'wkt': 'POINT(37.428 -122.095)'},
    {'name': 'Point4', 'wkt': 'POINT(37.430 -122.100)'}
]

# Преобразование WKT в координаты и добавление точек на карту
for point in observation_points:
    geom = wkt.loads(point['wkt'])
    folium.Marker([geom.y, geom.x], popup=point['name']).add_to(m)

# Сохранение карты
m.save("179.html")