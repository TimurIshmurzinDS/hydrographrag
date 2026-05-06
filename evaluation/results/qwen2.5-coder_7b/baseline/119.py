import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap

# Пример данных (замените на реальные данные)
data = {
    'River': ['Byzhy', 'Tekeli'],
    'Temperature': [15, 20],
    'pH': [7.2, 6.8],
    'Dissolved Oxygen': [9, 8]
}

df = pd.DataFrame(data)

# Очистка данных (пример)
df['Temperature'] = df['Temperature'].fillna(df['Temperature'].mean())
df['pH'] = df['pH'].fillna(df['pH'].mean())
df['Dissolved Oxygen'] = df['Dissolved Oxygen'].fillna(df['Dissolved Oxygen'].mean())

# Анализ данных
print("Статистический анализ:")
print(df.describe())

# Визуализация данных на карте
m = folium.Map(location=[48.37, 25.06], zoom_start=10)

# Добавление точек для каждого ручья
folium.Marker([48.37, 25.06], popup='Byzhy', icon=folium.Icon(color='red')).add_to(m)
folium.Marker([48.38, 25.07], popup='Tekeli', icon=folium.Icon(color='blue')).add_to(m)

# Добавление теплового картографа (пример)
heatmap_data = [
    [48.37, 25.06, df.loc[df['River'] == 'Byzhy', 'Temperature'].mean()],
    [48.38, 25.07, df.loc[df['River'] == 'Tekeli', 'Temperature'].mean()]
]
HeatMap(heatmap_data).add_to(m)

# Сохранение карты
m.save("119.html")