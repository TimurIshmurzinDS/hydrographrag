import pandas as pd
import folium
from datetime import datetime

# Предположим, что у нас есть CSV файл с данными о расходе воды
# Файл должен содержать столбцы: 'date' (дата) и 'discharge' (расход воды)
data = pd.read_csv('uzyn_kargaly_discharge.csv', parse_dates=['date'])

# Фильтрация данных для весеннего паводка (март-апрель)
spring_flood_data = data[(data['date'].dt.month >= 3) & (data['date'].dt.month <= 4)]

# Предположим, что у нас есть координаты реки Uzyn Kargaly River
river_coordinates = [42.8571, 76.9062]  # Примерные координаты

# Создание карты с использованием folium
m = folium.Map(location=river_coordinates, zoom_start=10)

# Добавление маркера на карту для местоположения реки
folium.Marker(
    location=river_coordinates,
    popup='Uzyn Kargaly River',
    icon=folium.Icon(color='blue')
).add_to(m)

# Вывод значений расхода воды во время весеннего паводка
print("Значения расхода воды во время весеннего паводка:")
for index, row in spring_flood_data.iterrows():
    print(f"Дата: {row['date']}, Расход воды: {row['discharge']} м³/с")

# Сохранение карты в файл
m.save("29.html")