import folium
from datetime import datetime

# Пример данных о колебаниях реки (температура воды)
water_temperature_data = {
    '2023-01-01': 5,
    '2023-02-01': 7,
    '2023-03-01': 9,
    '2023-04-01': 11,
    '2023-05-01': 13,
    '2023-06-01': 15,
    '2023-07-01': 17,
    '2023-08-01': 19,
    '2023-09-01': 17,
    '2023-10-01': 15,
    '2023-11-01': 13,
    '2023-12-01': 11
}

# Создание карты
m = folium.Map(location=[47.6062, -122.3321], zoom_start=13)

# Добавление маркера реки Каскелен
folium.Marker([47.6062, -122.3321], popup='Каскелен').add_to(m)

# Добавление слоя тепловых карт для отображения изменений температуры воздуха
for date, temp in water_temperature_data.items():
    folium.CircleMarker(
        location=[47.6062, -122.3321],
        radius=5,
        popup=f'Дата: {date}<br>Температура воды: {temp}°C',
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)

# Сохранение карты
m.save("240.html")