import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для визуализации)
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

# Пример данных о текущем уровне воды (замените на реальные данные)
water_level_data = [
    {'name': 'Shyzhyn River', 'level': 150, 'safe_limit': 140}
]

# Добавление точек с уровнями воды на карту
for data in water_level_data:
    if data['name'] == 'Shyzhyn River':
        if data['level'] > data['safe_limit']:
            folium.Marker([centroid.y, centroid.x], popup=f"Высокий уровень воды: {data['level']} м", icon=folium.Icon(color='red')).add_to(m)
        else:
            folium.Marker([centroid.y, centroid.x], popup=f"Уровень воды в норме: {data['level']} м", icon=folium.Icon(color='green')).add_to(m)

# Сохранение карты
m.save("28.html")