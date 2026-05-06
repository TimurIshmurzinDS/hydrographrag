import pandas as pd
from datetime import datetime
import numpy as np
import folium

# Шаг 1: Подготовка данных
koksu_river_data = pd.read_csv('koksu_river_data.csv')

# Шаг 2: Подготовка данных для моделирования
koksu_river_data['date'] = pd.to_datetime(koksu_river_data['date'])
koksu_river_data['water_level'] = koksu_river_data['water_level'].astype(float)

# Шаг 3: Определение порога 50-летнего паводка
threshold = np.percentile(koksu_river_data['water_level'], 95)

# Шаг 4: Рассчет вероятности превышения порога
probability = (koksu_river_data['water_level'] > threshold).mean()

print(f'Вероятность превышения порога 50-летнего паводка: {probability:.2f}')

# Шаг 5: Визуализация результатов
m = folium.Map(location=[42.0, 74.0], zoom_start=10)
folium.Marker([42.0, 74.0], popup='Порог 50-летнего паводка').add_to(m)
folium.Marker([42.0, 74.0], popup=f'Вероятность превышения порога: {probability:.2f}').add_to(m)

m.save('203.html')