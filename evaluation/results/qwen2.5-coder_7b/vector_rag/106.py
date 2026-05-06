import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассина
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассина
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассина на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных уровней воды (замените на реальные данные)
water_levels = [
    {'name': 'Sarykan River', 'level': 150},
    {'name': 'Aksu River', 'level': 140}
]

# Добавление точек с уровнями воды на карту
for level in water_levels:
    folium.Marker(
        location=[centroid.y, centroid.x], 
        popup=f"{level['name']}: {level['level']} м",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("106.html")