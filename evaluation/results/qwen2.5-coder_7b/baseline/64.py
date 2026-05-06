import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка данных
data = pd.read_csv('sensor_data_tentek_river.csv')

# Проверка целостности данных
print(data.info())
print(data.describe())

# Анализ данных (пример: построение графиков)
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(data['timestamp'], data['temperature'], label='Temperature')
plt.xlabel('Timestamp')
plt.ylabel('Temperature (°C)')
plt.title('Temperature over Time')
plt.legend()
plt.show()

# Визуализация данных на карте
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)

sensor_data = {
    "type": "FeatureCollection",
    "features": []
}

for index, row in data.iterrows():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row['longitude'], row['latitude']]
        },
        "properties": {
            "time": row['timestamp'],
            "temperature": row['temperature'],
            "water_level": row['water_level']
        }
    }
    sensor_data["features"].append(feature)

TimestampedGeoJson(sensor_data, period="PT1M", add_last_point=True).add_to(m)

# Сохранение карты
m.save("64.html")