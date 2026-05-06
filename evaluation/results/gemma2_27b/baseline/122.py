import pandas as pd
import folium

# 1. Загрузка данных
data = pd.read_csv("river_data.csv") # Заменить "river_data.csv" на имя файла с данными

# 2. Обработка данных
water_level = data["water_level"]
date_time = data["date_time"]

# 3. Расчет пикового уровня
peak_level = water_level.max()

# 4. Расчет среднего многолетнего уровня
average_level = water_level.mean()

# 5. Сравнение значений
difference = peak_level - average_level

print(f"Пиковый уровень воды: {peak_level}")
print(f"Средний многолетний уровень: {average_level}")
print(f"Разница между пиковым и средним уровнем: {difference}")

# 6. Визуализация (необязательно)
m = folium.Map(location=[43.85, 76.91], zoom_start=12) # Заменить координаты на координаты реки Kishi Almaty River

folium.Marker(location=[43.85, 76.91], popup="Пиковый уровень").add_to(m)
m.save("122.html")