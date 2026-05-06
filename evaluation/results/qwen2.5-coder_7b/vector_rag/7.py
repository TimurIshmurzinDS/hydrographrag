import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реке Batareyka River (если доступны)
# Пример использования координат для представления текущего состояния
coordinates = [
    {'lat': 56.0, 'lon': 84.0, 'level': 120},  # Пример координат и уровня воды
    {'lat': 56.1, 'lon': 84.1, 'level': 130}
]

# Создание карты с центром в реке Batareyka River
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы ручья на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Добавление данных уровня воды на карту
for coord in coordinates:
    folium.Marker(
        location=[coord['lat'], coord['lon']],
        popup=f"Уровень воды: {coord['level']} см",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("7.html")