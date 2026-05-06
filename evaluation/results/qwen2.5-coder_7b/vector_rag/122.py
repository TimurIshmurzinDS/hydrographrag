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

# Пример данных уровня воды (замените на реальные данные)
water_level_data = [
    {'date': '2021-01-01', 'value': 50},
    {'date': '2021-02-01', 'value': 60},
    {'date': '2021-03-01', 'value': 70},
    {'date': '2021-04-01', 'value': 80},
    {'date': '2021-05-01', 'value': 90}
]

# Нахождение пикового уровня воды
peak_water_level = max(water_level_data, key=lambda x: x['value'])['value']

# Расчет среднего многолетнего показателя уровня воды
mean_water_level = sum(item['value'] for item in water_level_data) / len(water_level_data)

# Вывод результатов
print(f"Пиковый уровень воды на Kishi Almaty River: {peak_water_level}")
print(f"Средний многолетний показатель уровня воды: {mean_water_level}")

# Сохранение карты
m.save("122.html")