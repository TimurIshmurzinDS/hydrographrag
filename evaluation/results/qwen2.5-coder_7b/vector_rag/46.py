import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границы ручья Sarykan River
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре границы ручья
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы ручья на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных уровней воды (замените на реальные данные)
water_level_data_2022 = [
    {'date': '2022-01-01', 'value': 50},
    {'date': '2022-02-01', 'value': 60},
    {'date': '2022-03-01', 'value': 70}
]

water_level_data_2023 = [
    {'date': '2023-01-01', 'value': 55},
    {'date': '2023-02-01', 'value': 65},
    {'date': '2023-03-01', 'value': 75}
]

# Добавление точек уровней воды на карту
for data in water_level_data_2022:
    folium.Marker([centroid.y, centroid.x], popup=f"Уровень воды в 2022: {data['value']}", icon=folium.Icon(color='blue')).add_to(m)

for data in water_level_data_2023:
    folium.Marker([centroid.y, centroid.x], popup=f"Уровень воды в 2023: {data['value']}", icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("46.html")