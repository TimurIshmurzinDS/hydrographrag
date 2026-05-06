import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна реки Эмель
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в геометрии бассейна и использованием тайлов CartoDB positron
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Создание списка притоков (в данном случае только река Сарыкан)
prongs = [
    {'name': 'Сарыкан', 'geometry': wkt.loads('LINESTRING(45.123 78.901, 46.234 79.012)')}
]

# Добавление притоков на карту
for prong in prongs:
    folium.GeoJson(prong['geometry'], style_function=lambda x: {
        'color': 'blue',
        'weight': 2,
        'opacity': 1
    }).add_to(m)

# Сохранение карты в файл
m.save("168.html")