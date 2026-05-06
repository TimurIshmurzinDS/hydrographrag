import numpy as np
import folium

# Уровень воды в реке Талгар (в метрах над уровнем моря)
water_level = 1000  # примерное значение, которое нужно заменить на фактическое

# Координаты геометрии реки Талгар
lat = 43.123456  # широта
lon = 76.789012  # долгота

# Рассчитываем индекс NDVI
ndvi = (water_level - 1000) / (water_level + 1000)

# Создаем карту с помощью библиотеки folium
m = folium.Map(location=[lat, lon], zoom_start=10)

# Добавляем слой с индексом NDVI на карту
folium.Marker([lat, lon], popup=f'NDVI: {ndvi}').add_to(m)

# Сохраняем карту в файл
m.save("270.html")