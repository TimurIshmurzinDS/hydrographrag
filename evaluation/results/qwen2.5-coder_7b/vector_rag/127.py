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
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных для уровня паводка (замените на реальные данные)
water_level_data = [
    {"date": "2023-01-01", "value": 5},
    {"date": "2023-01-02", "value": 6},
    {"date": "2023-01-03", "value": 7},
    # Добавьте больше данных по необходимости
]

# Извлечение значений уровня паводка
water_level_values = [data["value"] for data in water_level_data]

# Нахождение максимального и среднего значения уровня паводка
max_water_level = max(water_level_values)
mean_water_level = sum(water_level_values) / len(water_level_values)

# Рассчет разницы между максимальным и средним значением
difference = max_water_level - mean_water_level

print(f"Максимальный уровень паводка: {max_water_level}")
print(f"Средний уровень паводка: {mean_water_level}")
print(f"Разница между максимальным и средним уровнем паводка: {difference}")

# Сохранение карты
m.save("127.html")