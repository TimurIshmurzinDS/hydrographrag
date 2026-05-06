import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре геометрии бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Координаты уровней воды (пример)
water_level_points = [
    {'lat': centroid.y + 0.1, 'lon': centroid.x - 0.1, 'level': 5},
    {'lat': centroid.y + 0.2, 'lon': centroid.x + 0.1, 'level': 6},
    {'lat': centroid.y - 0.1, 'lon': centroid.x + 0.2, 'level': 4}
]

# Добавление маркеров уровней воды на карту
for point in water_level_points:
    folium.Marker(
        location=[point['lat'], point['lon']],
        popup=f"Уровень воды: {point['level']} м",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("67.html")