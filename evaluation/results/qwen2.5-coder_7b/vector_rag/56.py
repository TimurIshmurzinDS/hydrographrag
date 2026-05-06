import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных наблюдений уровня воды (замените на реальные данные)
water_level_data = [
    {'date': '2018-01-01', 'level': 0.5},
    {'date': '2019-01-01', 'level': 0.6},
    {'date': '2020-01-01', 'level': 0.7},
    {'date': '2021-01-01', 'level': 0.8},
    {'date': '2022-01-01', 'level': 0.9}
]

# Добавление точек наблюдений уровня воды на карту
for data in water_level_data:
    folium.Marker([centroid.y, centroid.x], popup=f"Уровень воды: {data['level']}").add_to(m)

# Сохранение карты
m.save("56.html")