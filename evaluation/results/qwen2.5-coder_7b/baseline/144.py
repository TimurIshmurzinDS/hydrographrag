import pandas as pd
import folium

# Пример данных: CSV файл с информацией о датчиках уровня воды
data = {
    'sensor_id': [1, 2, 3],
    'latitude': [55.7494, 55.7500, 55.7506],
    'longitude': [37.6180, 37.6185, 37.6190],
    'water_level': [2.5, 3.0, 2.8]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Установка пределов уровня воды (например, 3.0 метров)
threshold = 3.0

# Определение оповещений
df['alert'] = df['water_level'] > threshold

# Визуализация данных на карте
m = folium.Map(location=[55.7494, 37.6180], zoom_start=12)

for index, row in df.iterrows():
    if row['alert']:
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Sensor ID: {row['sensor_id']}, Water Level: {row['water_level']} m (Alert!)",
            icon=folium.Icon(color='red', icon='warning')
        ).add_to(m)
    else:
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Sensor ID: {row['sensor_id']}, Water Level: {row['water_level']} m",
            icon=folium.Icon(color='green', icon='info-sign')
        ).add_to(m)

# Сохранение карты
m.save("144.html")