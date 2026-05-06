import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для информации)
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

# Пример данных для параметра температуры воды (замените на реальные данные)
data_2021 = [
    {'date': '2021-01-01', 'temperature': 15},
    {'date': '2021-02-01', 'temperature': 16},
    {'date': '2021-03-01', 'temperature': 17}
]

data_2022 = [
    {'date': '2022-01-01', 'temperature': 14},
    {'date': '2022-02-01', 'temperature': 15},
    {'date': '2022-03-01', 'temperature': 16}
]

# Вычисление средних значений температуры
mean_temp_2021 = sum(item['temperature'] for item in data_2021) / len(data_2021)
mean_temp_2022 = sum(item['temperature'] for item in data_2022) / len(data_2022)

# Вывод результатов сравнения
print(f"Средняя температура в 2021 году: {mean_temp_2021}°C")
print(f"Средняя температура в 2022 году: {mean_temp_2022}°C")

# Сохранение карты
m.save("53.html")