import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границ бассейна из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центре границы бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат гидрологических постов (WKT) на реке Sharyn River
# Эти данные должны быть заменены реальными данными из источника
hydro_posts = [
    {'name': 'Post1', 'geometry': wkt.loads('POINT(43.2056 76.8912)')},
    {'name': 'Post2', 'geometry': wkt.loads('POINT(43.2100 76.8950)')},
    {'name': 'Post3', 'geometry': wkt.loads('POINT(43.2125 76.8975)')}
]

# Добавление гидрологических постов на карту
for post in hydro_posts:
    folium.Marker([post['geometry'].y, post['geometry'].x], popup=post['name']).add_to(m)

# Сохранение карты в файл
m.save("70.html")