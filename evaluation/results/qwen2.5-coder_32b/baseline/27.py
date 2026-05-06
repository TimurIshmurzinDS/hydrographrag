import pandas as pd
import folium
from datetime import datetime

# Предположим, что у нас есть CSV-файл с данными о расходе воды для реки Batareyka River.
# Файл содержит столбцы: 'date' (дата), 'discharge' (расход воды).

# Шаг 1: Загрузка данных
data = pd.read_csv('batareyka_river_discharge.csv', parse_dates=['date'])

# Шаг 2: Фильтрация данных за период весеннего таяния (март-апрель)
spring_melt_data = data[(data['date'].dt.month >= 3) & (data['date'].dt.month <= 4)]

# Предположим, что у нас есть координаты реки Batareyka River
river_coordinates = [56.1290, 47.2825]  # Примерные координаты

# Шаг 3: Создание карты с использованием folium
m = folium.Map(location=river_coordinates, zoom_start=10)

# Добавление маркера на карту с информацией о расходе воды
folium.Marker(
    location=river_coordinates,
    popup=f"Средний расход воды: {spring_melt_data['discharge'].mean():.2f} м³/с",
    tooltip="Наведите, чтобы узнать средний расход воды"
).add_to(m)

# Шаг 4: Добавление временной линии на карту (если необходимо)
for _, row in spring_melt_data.iterrows():
    folium.CircleMarker(
        location=river_coordinates,
        radius=row['discharge'] / 10,  # Масштабируем радиус для наглядности
        color='blue',
        fill=True,
        fill_color='blue',
        popup=f"Дата: {row['date'].strftime('%Y-%m-%d')}, Расход воды: {row['discharge']} м³/с"
    ).add_to(m)

# Шаг 5: Сохранение карты в файл
m.save("27.html")

print("Карта сохранена как 27.html")