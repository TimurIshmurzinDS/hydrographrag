import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реках из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в centroid basin_data
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о реках (если они доступны в виде WKT)
rivers = [
    {'name': 'Urzhar River', 'geometry': wkt.loads('POLYGON((...))')},
    {'name': 'Byzhy River', 'geometry': wkt.loads('POLYGON((...))')}
]

# Добавление рек на карту
for river in rivers:
    folium.GeoJson(river['geometry'].to_json(), style_function=lambda x: {
        'color': 'blue',
        'weight': 2,
        'fillOpacity': 0.5
    }).add_to(m)

# Сохранение карты
m.save("199.html")