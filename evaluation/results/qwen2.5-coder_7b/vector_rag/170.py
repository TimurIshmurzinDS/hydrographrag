import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границы бассейна из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат для ручья Терисбутак и его связанных артерий (WKT)
river_coords = [
    {'name': 'Terisbuthak Creek', 'wkt': 'POINT(123.456 78.901)'},
    {'name': 'Artery1', 'wkt': 'LINESTRING(123.456 78.901, 124.567 79.012)'},
    {'name': 'Artery2', 'wkt': 'LINESTRING(123.456 78.901, 125.678 79.123)'}
]

# Добавление ручья и артерий на карту
for river in river_coords:
    geom = wkt.loads(river['wkt'])
    folium.Marker([geom.y, geom.x], popup=river['name']).add_to(m)
    if isinstance(geom, gpd.GeoSeries):
        for line in geom:
            folium.PolyLine(line.coords, color='blue', weight=2.5).add_to(m)

# Сохранение карты
m.save("170.html")