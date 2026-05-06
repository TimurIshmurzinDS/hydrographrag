import pandas as pd
import numpy as np
import folium
from scipy.stats import zscore

# Предположим, что у нас есть данные в формате CSV
# Структура данных: timestamp, sensor_id, location_lat, location_lon, value

# Загрузка данных
data = pd.read_csv('monitoring_data.csv', parse_dates=['timestamp'])

# Проверка первых строк данных
print(data.head())

# Предварительная обработка данных
# Удаление пропусков
data.dropna(inplace=True)

# Вычисление z-оценки для каждого датчика
data['z_score'] = data.groupby('sensor_id')['value'].transform(zscore)

# Определение сбоев (например, значения z-оценки больше 3 или меньше -3)
outliers = data[(data['z_score'] > 3) | (data['z_score'] < -3)]

# Визуализация на карте
m = folium.Map(location=[54.7109, 20.5111], zoom_start=8)  # Координаты Киши Осек

# Добавление маркеров для сбоев
for idx, row in outliers.iterrows():
    folium.Marker(
        location=[row['location_lat'], row['location_lon']],
        popup=f"Sensor ID: {row['sensor_id']}, Timestamp: {row['timestamp']}, Value: {row['value']}",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты
m.save("142.html")

print("Карта сохранена как 142.html")