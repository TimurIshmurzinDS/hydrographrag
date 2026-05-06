import pandas as pd
import matplotlib.pyplot as plt
from folium import Map, Marker

# Шаг 1: Сбор данных
koksu_data = pd.read_csv('koksu_river_water_levels.csv')
emel_data = pd.read_csv('emel_river_water_levels.csv')

# Шаг 2: Предварительная обработка данных
koksu_data['date'] = pd.to_datetime(koksu_data['date'])
emel_data['date'] = pd.to_datetime(emel_data['date'])

# Шаг 3: Агрегация данных
koksu_monthly = koksu_data.groupby(pd.Grouper(key='date', freq='M')).mean()
emel_monthly = emel_data.groupby(pd.Grouper(key='date', freq='M')).mean()

# Шаг 4: Визуализация данных
plt.plot(koksu_monthly['water_level'], label='Koksu River')
plt.plot(emel_monthly['water_level'], label='Emel River')
plt.xlabel('Month')
plt.ylabel('Water Level (m)')
plt.title('Historical Water Levels in Koksu and Emel Rivers')
plt.legend()
plt.show()

# Создание карты с помощью библиотеки folium
m = Map(location=[43.2, 76.9], zoom_start=8)

# Добавить маркеры для обеих рек на карту
Marker([43.15, 76.85]).add_to(m)
Marker([43.35, 77.05]).add_to(m)

m.save("196.html")