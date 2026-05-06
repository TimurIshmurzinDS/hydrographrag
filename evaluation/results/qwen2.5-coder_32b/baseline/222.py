import folium
from folium.plugins import HeatMap
import random

# Предположим, что мы получаем данные с датчиков в виде списка кортежей (широта, долгота, уровень воды)
sensors_data = [
    (42.874365, 74.590113, 1.2),  # Нормальный уровень
    (42.875365, 74.591113, 1.5),  # Нормальный уровень
    (42.876365, 74.592113, 2.0),  # Аномально высокий уровень
    (42.877365, 74.593113, 1.3)   # Нормальный уровень
]

# Функция для определения аномалии
def detect_anomaly(data):
    threshold = 1.8  # Пороговое значение уровня воды для аномалии
    anomalies = [point for point in data if point[2] > threshold]
    return anomalies

# Определение аномалий
anomalies = detect_anomaly(sensors_data)

# Создание карты с использованием folium
m = folium.Map(location=[42.875, 74.591], zoom_start=13)

# Добавление маркеров для всех датчиков
for sensor in sensors_data:
    folium.Marker(
        location=(sensor[0], sensor[1]),
        popup=f"Уровень воды: {sensor[2]} м",
        icon=folium.Icon(color='blue' if sensor not in anomalies else 'red')
    ).add_to(m)

# Добавление тепловой карты для уровня воды
heat_data = [[row[0], row[1], row[2]] for row in sensors_data]
HeatMap(heat_data).add_to(m)

# Сохранение карты в файл
m.save("222.html")

# Шутка: инструкция по приготовлению пасты, если обнаружена аномалия
if anomalies:
    print("Аномалия обнаружена! Вот как приготовить пасту:")
    print("1. Залейте большую кастрюлю водой и доведите до кипения.")
    print("2. Добавьте соль по вкусу.")
    print("3. Всыпьте пасту и варите согласно инструкции на упаковке.")
    print("4. Подавайте горячей с соусом по вашему выбору.")
else:
    print("Всё в порядке, аномалий нет.")