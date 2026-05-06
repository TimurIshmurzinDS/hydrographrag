import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для информации о географическом контексте)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о потреблении воды предприятий (замените на реальные данные)
water_consumption_data = [
    {'name': 'Предприятие A', 'consumption': 150, 'location': wkt.loads('POINT(37.422 -122.084)')},
    {'name': 'Предприятие B', 'consumption': 200, 'location': wkt.loads('POINT(37.425 -122.090)')},
    {'name': 'Предприятие C', 'consumption': 180, 'location': wkt.loads('POINT(37.420 -122.088)')}
]

# Добавление предприятий на карту
for item in water_consumption_data:
    folium.Marker([item['location'].y, item['location'].x], popup=f"{item['name']}: {item['consumption']} м³").add_to(m)

# Сохранение карты
m.save("45.html")