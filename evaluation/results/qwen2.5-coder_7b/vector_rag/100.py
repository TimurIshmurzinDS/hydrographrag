import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне (только для визуализации)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.to_crs(epsg=4326, inplace=True)

# Инициализация карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о промежуточных звеньях (WKT)
intermediate_rivers = [
    {'name': 'Bizhy', 'geometry': wkt.loads('LINESTRING(37.12345 48.65432, 37.23456 48.76543)')},
    {'name': 'Shynzhaly', 'geometry': wkt.loads('LINESTRING(37.34567 48.87654, 37.45678 48.98765)')},
    {'name': 'Prokhodnaya', 'geometry': wkt.loads('LINESTRING(37.56789 49.01234, 37.67890 49.12345)')}
]

# Добавление промежуточных звеньев на карту
for river in intermediate_rivers:
    folium.GeoJson(river['geometry'].to_json(), style_function=lambda x: {
        'color': 'blue',
        'weight': 2,
        'opacity': 0.7
    }).add_to(m)

# Сохранение карты
m.save("100.html")