import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Темирлик
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что координаты реки и деревни известны в формате WKT
# Для примера создадим список словарей с координатами (в реальности эти данные должны быть предоставлены)
coordinates = [
    {'name': 'Temirlik River', 'wkt': 'LINESTRING(76.90 42.85, 76.91 42.86)'},
    {'name': 'Temirlik village', 'wkt': 'POINT(76.905 42.855)'}
]

# Добавление точек на карту
for coord in coordinates:
    geom = wkt.loads(coord['wkt'])
    folium.Marker(
        location=[geom.y, geom.x],
        popup=coord['name'],
        icon=folium.Icon(color='blue' if 'River' in coord['name'] else 'red')
    ).add_to(m)

# Сохранение карты в файл
m.save("66.html")