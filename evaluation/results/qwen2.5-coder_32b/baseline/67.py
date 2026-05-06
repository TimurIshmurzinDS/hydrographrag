import pandas as pd
import folium

# Шаг 1: Загрузка данных
# Предположим, что данные находятся в файле 'water_levels.csv'
data = pd.read_csv('water_levels.csv')

# Пример структуры CSV файла:
# post_id,latitude,longitude,timestamp,water_level
# 1,53.2045,34.3698,2023-10-01 12:00:00,150.5
# 2,53.2050,34.3700,2023-10-01 12:05:00,151.0

# Шаг 2: Фильтрация для получения последних записей с каждого поста
latest_data = data.sort_values(by='timestamp').drop_duplicates(subset='post_id', keep='last')

# Шаг 3: Подготовка данных к визуализации
# Создание списка кортежей (широта, долгота, уровень воды)
locations = latest_data[['latitude', 'longitude', 'water_level']].values.tolist()

# Шаг 4: Визуализация на карте с использованием folium
m = folium.Map(location=[53.205, 34.37], zoom_start=13)

for lat, lon, water_level in locations:
    folium.Marker(
        location=[lat, lon],
        popup=f'Уровень воды: {water_level} см',
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Шаг 5: Сохранение карты в HTML-файл
m.save("67.html")