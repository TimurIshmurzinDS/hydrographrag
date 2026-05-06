import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import folium
from folium.plugins import MarkerCluster

# Шаг 1: Загрузка данных
data = pd.read_csv('sensor_data.csv', parse_dates=['timestamp'])

# Предположим, что данные имеют следующую структуру:
# timestamp, sensor_id, latitude, longitude, value

# Шаг 2: Предварительный анализ данных
print(data.head())
print(data.info())

# Проверка пропущенных значений
print(data.isnull().sum())

# Заполнение пропущенных значений (если необходимо)
data.fillna(method='ffill', inplace=True)

# Шаг 3: Визуализация временных рядов
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 7))
for sensor_id in data['sensor_id'].unique():
    sensor_data = data[data['sensor_id'] == sensor_id]
    plt.plot(sensor_data['timestamp'], sensor_data['value'], label=f'Sensor {sensor_id}')
plt.title('Показания сенсоров на реке Прокходная')
plt.xlabel('Время')
plt.ylabel('Значение')
plt.legend()
plt.show()

# Шаг 4: Обнаружение аномалий
# Используем Isolation Forest для обнаружения аномалий
iso_forest = IsolationForest(contamination=0.1, random_state=42)
data['anomaly'] = iso_forest.fit_predict(data[['value']])
data['anomaly'] = data['anomaly'].map({1: 0, -1: 1})  # Приводим к бинарному формату (0 - норма, 1 - аномалия)

# Шаг 5: Визуализация результатов на карте
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)
marker_cluster = MarkerCluster().add_to(m)

for _, row in data[data['anomaly'] == 1].iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Sensor ID: {row['sensor_id']}<br>Value: {row['value']}<br>Anomaly: Yes",
        icon=folium.Icon(color='red')
    ).add_to(marker_cluster)

# Шаг 6: Сохранение карты
m.save("74.html")