import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Инициализация карты с центром масс бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление географических границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Координаты центра масс для каждой из трех рек (примерные значения)
coordinates = [
    {'name': 'Byzhy River', 'wkt': 'POINT(37.5641 48.9823)'},
    {'name': 'Kurty River', 'wkt': 'POINT(37.0123 48.5678)'},
    {'name': 'Urzhar River', 'wkt': 'POINT(36.7890 48.1234)'}
]

# Добавление маркеров уровней водопотребления на карту
for coord in coordinates:
    point = wkt.loads(coord['wkt'])
    folium.Marker([point.y, point.x], popup=f"{coord['name']} - Уровень водопотребления: [Ваше значение]").add_to(m)

# Сохранение карты в файл
m.save("112.html")