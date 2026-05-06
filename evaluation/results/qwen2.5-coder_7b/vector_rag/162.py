import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат для визуализации (если есть)
coordinates = [
    {'name': 'Bayankol village', 'geometry': wkt.loads('POINT(105.1234 47.5678)')},
    {'name': 'Lepsy River mouth', 'geometry': wkt.loads('POINT(105.9876 47.1234)')}
]

# Добавление точек на карту
for coord in coordinates:
    folium.Marker([coord['geometry'].y, coord['geometry'].x], popup=coord['name']).add_to(m)

# Сохранение карты
m.save("162.html")