import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для контекста)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат из наблюдений (замените на реальные данные)
coordinates = [
    {'lat': 45.123, 'lon': -122.456},
    {'lat': 45.789, 'lon': -123.012},
    {'lat': 46.345, 'lon': -124.567}
]

# Добавление точек на карте
for coord in coordinates:
    folium.Marker([coord['lat'], coord['lon']], popup='Observation').add_to(m)

# Сохранение карты
m.save("248.html")