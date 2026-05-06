import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление региона в карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат реки Дос (WKT)
river_coordinates = [
    {'name': 'Дос', 'wkt': 'LINESTRING(105.3456 47.8901, 105.3457 47.8902, 105.3458 47.8903)'}
]

# Добавление координат реки на карту
for coord in river_coordinates:
    folium.GeoJson(wkt.loads(coord['wkt']), style_function=lambda x: {
        'color': 'blue',
        'weight': 2,
        'opacity': 1
    }).add_to(m)

# Сохранение карты в файл
m.save("252.html")