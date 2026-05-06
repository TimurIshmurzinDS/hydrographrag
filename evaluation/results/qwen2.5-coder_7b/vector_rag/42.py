import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile и параметрами tiles='CartoDB positron'
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границы ровнинки в карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат (WKT) для наглядности
coordinates = [
    {'name': 'Поле 1', 'wkt': 'POINT(37.422 -122.084)', 'water_consumption': 100},
    {'name': 'Поле 2', 'wkt': 'POINT(37.425 -122.086)', 'water_consumption': 150}
]

# Добавление маркеров с данными о потреблении воды
for coord in coordinates:
    point = wkt.loads(coord['wkt'])
    folium.Marker([point.y, point.x], popup=f"{coord['name']}: {coord['water_consumption']} м³").add_to(m)

# Сохранение карты в файл "42.html"
m.save("42.html")