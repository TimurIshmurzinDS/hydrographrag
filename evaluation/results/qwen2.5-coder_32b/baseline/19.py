import pandas as pd
from datetime import datetime
import folium

# Предполагаем, что у нас есть CSV файл с гидрометрическими данными
# Структура файла: date (дата), water_level (уровень воды)

# Загрузка данных
data = pd.read_csv('osek_water_levels.csv', parse_dates=['date'])

# Определение периода весеннего паводка (март-апрель)
spring_flood_period = data[(data['date'].dt.month >= 3) & (data['date'].dt.month <= 4)]

# Нахождение максимального уровня воды за каждый год в периоде весеннего паводка
max_levels_per_year = spring_flood_period.groupby(spring_flood_period['date'].dt.year)['water_level'].max().reset_index()

# Определение последнего года с данными о паводке
last_year_with_data = max_levels_per_year['year'].max()
max_water_level_last_year = max_levels_per_year[max_levels_per_year['year'] == last_year_with_data]['water_level'].values[0]

print(f"Максимальный уровень воды в реке Osek River за последний весенний паводок ({last_year_with_data} год): {max_water_level_last_year} м")

# Координаты реки Osek River (примерные)
osek_river_coords = [56.1290, 47.3830]

# Создание интерактивной карты с помощью folium
m = folium.Map(location=osek_river_coords, zoom_start=10)

# Добавление маркера с информацией о максимальном уровне воды
folium.Marker(
    location=osek_river_coords,
    popup=f"Максимальный уровень воды: {max_water_level_last_year} м",
    icon=folium.Icon(color='blue')
).add_to(m)

# Сохранение карты в файл
m.save("19.html")