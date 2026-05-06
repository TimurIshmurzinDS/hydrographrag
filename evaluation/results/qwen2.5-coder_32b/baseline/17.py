import pandas as pd
import folium
from folium.plugins import HeatMap

# Шаг 1: Сбор данных
# Предположим, что у нас есть CSV-файл с данными о расходе воды для реки Tekes River.
# Файл содержит столбцы: 'date', 'discharge' (расход воды), 'latitude', 'longitude'
data = pd.read_csv('tekes_river_discharge.csv')

# Шаг 2: Обработка данных
# Преобразуем даты и фильтруем данные за весенний период (март-май)
data['date'] = pd.to_datetime(data['date'])
spring_data = data[(data['date'].dt.month >= 3) & (data['date'].dt.month <= 5)]

# Шаг 3: Визуализация на карте
# Создаем базовую карту с центром в районе реки Tekes River
m = folium.Map(location=[42.86, 79.10], zoom_start=10)

# Добавляем точки с данными о расходе воды
for _, row in spring_data.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=row['discharge'] / 50,  # Масштабируем радиус для лучшей визуализации
        color='blue',
        fill=True,
        fill_color='blue',
        popup=f"Дата: {row['date'].strftime('%Y-%m-%d')}\nРасход воды: {row['discharge']} м³/с"
    ).add_to(m)

# Добавляем тепловую карту для более наглядного отображения плотности данных
heat_data = [[row['latitude'], row['longitude']] for _, row in spring_data.iterrows()]
HeatMap(heat_data).add_to(m)

# Шаг 4: Сохранение карты
m.save("17.html")