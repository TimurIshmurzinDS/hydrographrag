import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для информации)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о водных уровнях и потреблении воды (замените на реальные данные)
water_level_data = [
    {'date': '2023-01-01', 'water_level': 50},
    {'date': '2023-02-01', 'water_level': 55},
    {'date': '2023-03-01', 'water_level': 60},
    {'date': '2023-04-01', 'water_level': 65},
    {'date': '2023-05-01', 'water_level': 70}
]

water_consumption_data = [
    {'date': '2023-01-01', 'consumption': 100},
    {'date': '2023-02-01', 'consumption': 110},
    {'date': '2023-03-01', 'consumption': 120},
    {'date': '2023-04-01', 'consumption': 130},
    {'date': '2023-05-01', 'consumption': 140}
]

# Анализ данных о водных уровнях
water_level_values = [entry['water_level'] for entry in water_level_data]
dates = [entry['date'] for entry in water_level_data]

# Анализ данных о потреблении воды
consumption_values = [entry['consumption'] for entry in water_consumption_data]

# Визуализация данных на карте (пример: добавление маркеров с данными)
for i, date in enumerate(dates):
    folium.Marker(
        location=[centroid.y, centroid.x],
        popup=f"Дата: {date}<br>Водный уровень: {water_level_values[i]}<br>Потребление воды: {consumption_values[i]}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("272.html")