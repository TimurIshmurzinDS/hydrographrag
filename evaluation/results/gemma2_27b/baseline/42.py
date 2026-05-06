import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузка данных
agro = gpd.read_file("agrocultures.shp")  # Замените на путь к файлу с данными об агрокультурах
water_samples = gpd.read_file("water_samples.shp") # Замените на путь к файлу с данными о точках отбора проб

# Создание буферных зон
agro['buffer'] = agro.geometry.buffer(500)  # Создайте буферные зоны радиусом 500 метров

# Анализ пересечения
intersections = gpd.overlay(water_samples, agro[['buffer']], how='intersection')

# Статистический анализ (пример)
mean_nitrates_in_buffer = intersections['nitrates'].mean()
mean_nitrates_outside_buffer = water_samples[~water_samples.within(agro['buffer'].unary_union)]['nitrates'].mean()

print(f"Средняя концентрация нитратов в буферных зонах: {mean_nitrates_in_buffer}")
print(f"Средняя концентрация нитратов вне буферных зон: {mean_nitrates_outside_buffer}")

# Визуализация
m = folium.Map(location=[54.0, 37.0], zoom_start=10)  # Замените на координаты реки Лепси

# Добавление слоев
folium.GeoJson(agro).add_to(m)
folium.GeoJson(water_samples).add_to(m)
folium.GeoJson(intersections, style_function=lambda feature: {'fillColor': 'red'}).add_to(m)

# Сохранение карты
m.save("42.html")