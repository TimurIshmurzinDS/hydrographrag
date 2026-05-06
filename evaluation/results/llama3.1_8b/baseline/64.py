import pandas as pd
import folium

# Шаг 1: Загрузка данных
df = pd.read_csv('tentek_river_sensors.csv')

# Шаг 2: Подготовка данных
df['x'] = df['x'].astype(float)
df['y'] = df['y'].astype(float)

# Шаг 3: Анализ данных
anomalies = df[df['value'] > 100]  # Пример аномалии - значение измерения больше 100

# Шаг 4: Визуализация результатов
m = folium.Map(location=[df['y'].mean(), df['x'].mean()], zoom_start=10)

for index, row in anomalies.iterrows():
    folium.CircleMarker([row['y'], row['x']], radius=5, color='red').add_to(m)

folium.Marker([df['y'].mean(), df['x'].mean()], popup='Средние координаты сенсоров').add_to(m)
m.save("64.html")