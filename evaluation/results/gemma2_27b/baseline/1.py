import folium
import requests  # Для получения данных с API (если необходимо)

# Замените эти значения на актуальные данные
latitude = 43.25 # Широта точки измерения
longitude = 77.00 # Долгота точки измерения
water_level = 1.5 # Текущий уровень воды в метрах

# Создание карты
m = folium.Map(location=[latitude, longitude], zoom_start=10)

# Добавление маркера с информацией о уровне воды
folium.Marker(
    [latitude, longitude],
    popup=f"Текущий уровень воды: {water_level} м",
).add_to(m)

# Сохранение карты в HTML-файл
m.save("1.html")