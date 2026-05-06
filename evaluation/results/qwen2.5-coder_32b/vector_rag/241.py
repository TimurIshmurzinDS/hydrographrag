import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты с центроидом бассейна
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin.geometry.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим координаты для реки Талгар и города Талгар (это примерные данные)
coordinates = [
    {"name": "Талгарская река", "geometry": wkt.loads("POINT(76.9431 42.8500)")},
    {"name": "Талгар город", "geometry": wkt.loads("POINT(76.9431 42.8500)")}
]

# Добавление точек на карту
for coord in coordinates:
    folium.Marker(
        location=[coord['geometry'].y, coord['geometry'].x],
        popup=coord['name'],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("241.html")