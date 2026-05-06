import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для информации о границах)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о уровне воды (замените на реальные данные)
water_level_data = [
    {"name": "Ili River", "geometry": wkt.loads("POINT(74.5678 39.1234)"), "value": 100},
    {"name": "Near Ili", "geometry": wkt.loads("POINT(74.5789 39.1345)"), "value": 95}
]

# Добавление точек с уровнями воды на карту
for point in water_level_data:
    folium.Marker(
        location=[point['geometry'].y, point['geometry'].x],
        popup=f"Река: {point['name']}, Уровень воды: {point['value']} м",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("1.html")