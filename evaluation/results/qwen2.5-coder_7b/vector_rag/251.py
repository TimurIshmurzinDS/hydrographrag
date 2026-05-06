import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром на centroid базина
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление базина на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат для рисования реки (WKT)
river_coords = [
    {'name': 'Kumbel River', 'wkt': 'LINESTRING(10 10, 20 20, 30 40)'}
]

# Рисование реки на карте
for coord in river_coords:
    geom = wkt.loads(coord['wkt'])
    folium.GeoJson({'type': 'Feature', 'geometry': geom}, style_function=lambda x: {
        'color': 'blue',
        'weight': 2,
        'opacity': 1
    }).add_to(m)

# Сохранение карты в файл
m.save("251.html")