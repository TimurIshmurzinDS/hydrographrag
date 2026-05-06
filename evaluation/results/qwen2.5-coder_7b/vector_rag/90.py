import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Координаты рек (если они доступны в виде WKT)
rivers = [
    {'name': 'Karaoy River', 'wkt': 'POINT(39.165748 44.013333)'},
    {'name': 'Baskan River', 'wkt': 'POINT(39.200000 44.050000)'},
    {'name': 'Temirlik River', 'wkt': 'POINT(39.180000 44.070000)'}
]

# Добавление маркеров рек на карту
for river in rivers:
    point = wkt.loads(river['wkt'])
    folium.Marker([point.y, point.x], popup=f"{river['name']} - Риск затопления: Высокий").add_to(m)

# Сохранение карты
m.save("90.html")