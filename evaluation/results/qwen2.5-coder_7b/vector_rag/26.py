import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границы бассейна из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Наблюдения уровня воды (WKT)
observations = [
    {'wkt': 'POINT(10.5 48.3)', 'level': 1.2},
    {'wkt': 'POINT(10.6 48.4)', 'level': 1.3},
    {'wkt': 'POINT(10.7 48.5)', 'level': 1.4},
    {'wkt': 'POINT(10.8 48.6)', 'level': 1.5}
]

# Добавление маркеров для наблюдений уровня воды
for obs in observations:
    point = wkt.loads(obs['wkt'])
    folium.Marker([point.y, point.x], popup=f"Уровень воды: {obs['level']} м").add_to(m)

# Сохранение карты в файл
m.save("26.html")