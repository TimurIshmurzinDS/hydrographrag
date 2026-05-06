import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о ручье
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в centroid basin_data и заданием тайлов
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление ручья на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных наблюдений уровня воды (WKT)
water_level_data = [
    {'wkt': 'POINT(123.456 78.901)', 'date': '2023-04-01', 'value': 15},
    {'wkt': 'POINT(124.567 79.012)', 'date': '2023-04-02', 'value': 18},
    {'wkt': 'POINT(125.678 79.123)', 'date': '2023-04-03', 'value': 16}
]

# Фильтрация данных, чтобы выбрать только те наблюдения, которые выше нормального уровня
normal_level = 10  # Пример нормального уровня воды
high_water_levels = [point for point in water_level_data if wkt.loads(point['wkt']).within(basin_data.geometry[0]) and point['value'] > normal_level]

# Добавление точек с повышенным уровнем воды на карту
for point in high_water_levels:
    folium.Marker([point['wkt'].split()[1], point['wkt'].split()[2]], popup=f"Уровень воды: {point['value']} (Дата: {point['date']})", icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("148.html")