import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Определение координат полей для полива (пример данных)
fields_coordinates_wkt = [
    "POINT(51.0 71.0)",
    "POINT(51.1 71.1)",
    "POINT(51.2 71.2)"
]

# Создание списка словарей с координатами полей
fields_coordinates = [{'geometry': wkt.loads(coord)} for coord in fields_coordinates_wkt]

# Инициализация карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Добавление координат полей на карту
for field in fields_coordinates:
    folium.Marker([field['geometry'].y, field['geometry'].x], popup='Поле').add_to(m)

# Сохранение карты
m.save("266.html")