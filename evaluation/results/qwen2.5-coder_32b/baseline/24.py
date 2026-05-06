import pandas as pd
import folium

# Предположим, что у нас есть CSV-файл с историческими данными о уровне воды реки Улкен Алматы.
# Файл должен содержать столбцы: 'date', 'water_level', 'latitude', 'longitude'

# Загрузка данных
data = pd.read_csv('ulken_almaty_water_levels.csv')

# Преобразование даты в формат datetime
data['date'] = pd.to_datetime(data['date'])

# Фильтрация данных для весеннего периода (март-апрель)
spring_data = data[(data['date'].dt.month >= 3) & (data['date'].dt.month <= 4)]

# Создание карты с центром в районе реки Улкен Алматы
m = folium.Map(location=[42.8746, 75.1950], zoom_start=10)

# Добавление маркеров на карту для каждого измерения уровня воды
for _, row in spring_data.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=row['water_level'] / 10,  # Уменьшаем радиус для лучшей визуализации
        color='blue',
        fill=True,
        fill_color='blue',
        popup=f"Дата: {row['date'].strftime('%Y-%m-%d')}\nУровень воды: {row['water_level']} м"
    ).add_to(m)

# Сохранение карты в файл 24.html
m.save("24.html")