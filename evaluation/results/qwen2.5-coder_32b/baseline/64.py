import pandas as pd
import numpy as np
from scipy import stats
import folium

# Предполагаем, что данные находятся в CSV файле 'tentek_river_sensors.csv'
# Структура файла: sensor_id, latitude, longitude, timestamp, value

# Шаг 1: Сбор данных
data = pd.read_csv('tentek_river_sensors.csv', parse_dates=['timestamp'])

# Шаг 2: Предварительная обработка данных
data.dropna(subset=['value'], inplace=True)
z_scores = np.abs(stats.zscore(data['value']))
data_cleaned = data[z_scores < 3]  # Удаление выбросов с Z-оценкой > 3

# Шаг 3: Анализ статистики
sensor_stats = data_cleaned.groupby('sensor_id')['value'].agg(['mean', 'median', 'std']).reset_index()

# Шаг 4: Обнаружение аномалий
def detect_anomalies(sensor_data, threshold=3):
    z_scores = np.abs(stats.zscore(sensor_data['value']))
    return sensor_data[z_scores > threshold]

anomalies = data_cleaned.groupby('sensor_id').apply(detect_anomalies).reset_index(drop=True)

# Шаг 5: Визуализация результатов
m = folium.Map(location=[data_cleaned['latitude'].mean(), data_cleaned['longitude'].mean()], zoom_start=10)

for idx, row in data_cleaned.iterrows():
    color = 'green' if row['sensor_id'] not in anomalies['sensor_id'].values else 'red'
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        popup=f"Sensor ID: {row['sensor_id']}<br>Value: {row['value']}",
        color=color,
        fill=True,
        fill_color=color
    ).add_to(m)

m.save("64.html")