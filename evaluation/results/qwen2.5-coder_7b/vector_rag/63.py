import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для информации)
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

# Пример данных о гидропостах и их уровнях воды (замените на реальные данные)
hydro_stations = [
    {'name': 'Station1', 'geometry': wkt.loads('POINT(37.5 49)'), 'water_level': 20},
    {'name': 'Station2', 'geometry': wkt.loads('POINT(38.0 49)'), 'water_level': 25}
]

# Добавление гидропостов на карту
for station in hydro_stations:
    folium.Marker(
        location=[station['geometry'].y, station['geometry'].x],
        popup=f"{station['name']}: Уровень воды {station['water_level']} см",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("63.html")