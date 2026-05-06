import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре массы бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Координаты наблюдений (пример)
observations = [
    {'geometry': wkt.loads('POINT(37.123456 55.678901)'), 'value': 10},
    {'geometry': wkt.loads('POINT(37.123457 55.678902)'), 'value': 15},
    {'geometry': wkt.loads('POINT(37.123458 55.678903)'), 'value': 20},
    {'geometry': wkt.loads('POINT(37.123459 55.678904)'), 'value': 25}
]

# Добавление точек наблюдений на карту
for obs in observations:
    folium.Marker([obs['geometry'].y, obs['geometry'].x], popup=f"Значение: {obs['value']}").add_to(m)

# Сохранение карты в файл
m.save("12.html")