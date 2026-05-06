import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import folium

# Шаг 1: Сбор данных (пример загрузки из CSV файла)
# Предположим, что у нас есть файл 'osek_water_level.csv' с данными о уровне воды
data = pd.read_csv('osek_water_level.csv', parse_dates=['date'])

# Пример структуры данных:
# date                water_level
# 2023-01-01 00:00:00   150.0
# 2023-01-01 01:00:00   151.5
# ...

# Шаг 2: Обработка данных
data.set_index('date', inplace=True)

# Шаг 3: Анализ данных - определение периода паводка
# Предположим, что период паводка начинается, когда уровень воды превышает пороговое значение (например, 160 м)
threshold = 160.0
flood_period = data[data['water_level'] > threshold]

# Шаг 4: Моделирование уровня воды - прогнозирование текущего уровня воды в период паводка
# Простой пример с использованием последних данных за последние 24 часа
current_date = datetime.now()
last_24_hours = flood_period[flood_period.index > current_date - timedelta(days=1)]
predicted_water_level = last_24_hours['water_level'].mean()

print(f"Прогнозируемый уровень воды на реке Osek River в период паводка: {predicted_water_level} м")

# Шаг 5: Визуализация данных
# Координаты местоположения реки Osek (примерные координаты)
location = [46.9231, 38.0751]

m = folium.Map(location=location, zoom_start=10)

# Добавление маркера с текущим уровнем воды
folium.Marker(
    location,
    popup=f"Текущий уровень воды: {predicted_water_level} м",
    icon=folium.Icon(color='blue')
).add_to(m)

# Сохранение карты в файл
m.save("26.html")