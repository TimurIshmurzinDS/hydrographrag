import pandas as pd
import numpy as np
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка данных
data = pd.read_csv('sensor_data.csv')

# Проверка целостности данных
print("Количество пропущенных значений:")
print(data.isnull().sum())

# Удаление строк с пропущенными значениями (если необходимо)
data.dropna(inplace=True)

# Анализ временных рядов
data['timestamp'] = pd.to_datetime(data['timestamp'])
data.set_index('timestamp', inplace=True)

# Визуализация данных на карте
m = folium.Map(location=[56.0472, 37.189], zoom_start=13)

# Создание слоя для визуализации аномалий
anomalies = []
for index, row in data.iterrows():
    if row['value'] > 100:  # Пример условия для определения аномалии
        anomalies.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row['longitude'], row['latitude']]
            },
            "properties": {
                "time": index.strftime('%Y-%m-%dT%H:%M:%S'),
                "value": row['value']
            }
        })

# Добавление слоя аномалий на карту
TimestampedGeoJson(anomalies, period="PT1H", add_last_point=True).add_to(m)

# Сохранение карты
m.save("74.html")