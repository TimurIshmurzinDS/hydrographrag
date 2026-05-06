import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о границах водного бассейна
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Создание интерактивной карты с центром в центроиде водного бассейна
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin.to_json(), name="Водный бассейн", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты русла ручья Терисбутак и реки Талгар (примерные данные)
features = [
    {"name": "Терисбутак Creek", "wkt": "LINESTRING(76.95 43.01, 76.96 43.02)"},
    {"name": "Река Талгар", "wkt": "LINESTRING(76.98 43.00, 76.99 43.01)"}
]

# Добавление линий русла ручья и реки на карту
for feature in features:
    geom = wkt.loads(feature['wkt'])
    folium.GeoJson(gpd.GeoSeries(geom, crs='EPSG:4326').to_json(), name=feature['name'], style_function=lambda x: {'color': 'blue' if 'Терисбутак' in feature['name'] else 'red'}).add_to(m)

# Сохранение карты в файл
m.save("176.html")