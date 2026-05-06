import pandas as pd
import folium

# Пример данных (в реальности данные должны быть загружены из источника)
data = {
    'date': ['2021-06-01', '2021-07-01', '2021-08-01', '2021-09-01'],
    'max_flood_level': [3.5, 4.0, 4.5, 5.0],
    'historical_avg_level': [3.0, 3.2, 3.3, 3.4]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Преобразование столбца дат в формат datetime
df['date'] = pd.to_datetime(df['date'])

# Расчет разницы между максимальным уровнем паводка и историческим средним значением
df['difference'] = df['max_flood_level'] - df['historical_avg_level']

# Нахождение максимальной разницы
max_difference = df['difference'].max()

# Координаты реки Шарын (примерные)
sharyn_river_coords = [49.85, 73.2]

# Создание карты с использованием folium
m = folium.Map(location=sharyn_river_coords, zoom_start=10)

# Добавление маркера на карте с информацией о максимальной разнице
folium.Marker(
    location=sharyn_river_coords,
    popup=f"Максимальная разница между уровнем паводка и историческим средним значением: {max_difference:.2f} м",
    icon=folium.Icon(color='red')
).add_to(m)

# Сохранение карты в файл
m.save("127.html")

print(f"Максимальная разница между уровнем паводка и историческим средним значением: {max_difference:.2f} м")