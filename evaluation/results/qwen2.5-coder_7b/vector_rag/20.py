import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о потреблении воды и уровне воды (замените на реальные данные)
water_consumption_data = [
    {'date': '2023-06-01', 'consumption': 500},
    {'date': '2023-06-02', 'consumption': 600},
    {'date': '2023-06-03', 'consumption': 700},
    {'date': '2023-06-04', 'consumption': 800},
    {'date': '2023-06-05', 'consumption': 900}
]

water_level_data = [
    {'date': '2023-06-01', 'level': 1.2},
    {'date': '2023-06-02', 'level': 1.4},
    {'date': '2023-06-03', 'level': 1.6},
    {'date': '2023-06-04', 'level': 1.8},
    {'date': '2023-06-05', 'level': 2.0}
]

# Визуализация данных о потреблении воды
for data in water_consumption_data:
    folium.Marker([centroid.y, centroid.x], popup=f"Date: {data['date']}, Consumption: {data['consumption']} m³").add_to(m)

# Визуализация данных о уровне воды
for data in water_level_data:
    folium.Marker([centroid.y, centroid.x], popup=f"Date: {data['date']}, Level: {data['level']} m").add_to(m)

# Сохранение карты в файл
m.save("20.html")