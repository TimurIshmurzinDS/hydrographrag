import pandas as pd
import numpy as np
import folium
from datetime import datetime

# Шаг 1: Сбор данных (пример загрузки из CSV файла)
data = pd.read_csv('batareyka_river_monitoring.csv')

# Пример структуры данных:
# timestamp, sensor_id, latitude, longitude, water_level, flow_speed, water_quality
# 2023-10-01 12:00:00, S1, 54.8967, 37.6213, 1.2, 0.5, Good

# Шаг 2: Предварительная обработка данных
data['timestamp'] = pd.to_datetime(data['timestamp'])
data.dropna(inplace=True)

# Проверка на выбросы (простой пример)
for column in ['water_level', 'flow_speed']:
    mean = data[column].mean()
    std_dev = data[column].std()
    data = data[(data[column] > mean - 3 * std_dev) & (data[column] < mean + 3 * std_dev)]

# Шаг 3: Анализ временных рядов
def check_sensor_stability(sensor_data):
    if sensor_data.isnull().sum() > 0:
        return False
    return True

sensor_ids = data['sensor_id'].unique()
stable_sensors = []
unstable_sensors = []

for sensor in sensor_ids:
    sensor_data = data[data['sensor_id'] == sensor]['water_level']
    if check_sensor_stability(sensor_data):
        stable_sensors.append(sensor)
    else:
        unstable_sensors.append(sensor)

print(f"Стабильные датчики: {stable_sensors}")
print(f"Нестабильные датчики: {unstable_sensors}")

# Шаг 4: Визуализация данных
m = folium.Map(location=[54.8967, 37.6213], zoom_start=10)

for index, row in data.iterrows():
    color = 'green' if row['sensor_id'] in stable_sensors else 'red'
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"ID: {row['sensor_id']}<br>Уровень воды: {row['water_level']} м<br>Скорость течения: {row['flow_speed']} м/с<br>Качество воды: {row['water_quality']}",
        icon=folium.Icon(color=color)
    ).add_to(m)

m.save("14.html")