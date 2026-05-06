import pandas as pd
import numpy as np
from folium import Map, Marker
from folium.plugins import HeatMap

# Сбор и предобработка данных
data = {
    'Дата': ['2020-01-01', '2020-02-01', '2020-03-01'],
    'Температура (C)': [10, 15, 20],
    'Влажность (%)': [50, 60, 70]
}
df = pd.DataFrame(data)

# Анализ временных рядов
temp_mean = df['Температура (C)'].mean()
temp_std = df['Температура (C)'].std()

# Моделирование климата
mars_map = Map(location=[45, 0], zoom_start=2)
for i in range(len(df)):
    lat = np.random.uniform(40, 50)
    lon = np.random.uniform(-180, 180)
    marker = Marker([lat, lon], popup=f'Дата: {df["Дата"][i]}\nТемпература: {df["Температура (C)"][i]} C\nВлажность: {df["Влажность (%)"][i]} %')
    mars_map.add_child(marker)

# Визуализация результатов
m = HeatMap([[45, 0]], radius=10)
m.save("284.html")