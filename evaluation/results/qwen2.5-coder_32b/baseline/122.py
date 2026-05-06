import pandas as pd
import numpy as np
import folium

# Предположим, что у нас есть CSV-файл с данными о уровнях воды реки Kishi Almaty River.
# Файл должен содержать столбцы: 'date' (дата измерения), 'water_level' (уровень воды).

# Шаг 1: Сбор данных
data = pd.read_csv('kishi_almaty_water_levels.csv', parse_dates=['date'])

# Шаг 2: Обработка данных
# Проверка на пропущенные значения и удаление их, если они есть
data.dropna(subset=['water_level'], inplace=True)

# Шаг 3: Анализ данных
# Нахождение пикового уровня воды
peak_water_level = data['water_level'].max()

# Нахождение среднего многолетнего уровня воды
mean_water_level = data['water_level'].mean()

print(f"Пиковый уровень воды: {peak_water_level}")
print(f"Средний многолетний уровень воды: {mean_water_level}")

# Шаг 4: Визуализация результатов
# Предположим, что у нас есть координаты реки Kishi Almaty River.
river_coordinates = [43.2567, 76.9180]  # Примерные координаты

# Создание карты с помощью folium
m = folium.Map(location=river_coordinates, zoom_start=12)

# Добавление маркеров для пикового уровня и среднего многолетнего уровня
folium.Marker(
    location=river_coordinates,
    popup=f"Пиковый уровень воды: {peak_water_level}",
    icon=folium.Icon(color='red')
).add_to(m)

folium.Marker(
    location=river_coordinates,
    popup=f"Средний многолетний уровень воды: {mean_water_level}",
    icon=folium.Icon(color='blue')
).add_to(m)

# Сохранение карты в файл
m.save("122.html")