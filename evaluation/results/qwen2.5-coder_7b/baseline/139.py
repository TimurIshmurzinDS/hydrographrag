import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Загрузка данных (пример)
data = {
    'latitude': [51.234, 51.235, 51.236, 51.237, 51.238],
    'longitude': [71.123, 71.124, 71.125, 71.126, 71.127],
    'water_level': [10, 11, 12, 100, 11],  # Пример данных с аномалией
    'sensor_id': ['S1', 'S2', 'S3', 'S4', 'S5']
}
df = pd.DataFrame(data)

# Фильтрация данных для района реки Сарыкан (пример координат)
saraykan_area = {
    'min_lat': 51.230,
    'max_lat': 51.240,
    'min_lon': 71.120,
    'max_lon': 71.130
}

df_filtered = df[(df['latitude'] >= saraykan_area['min_lat']) &
                 (df['latitude'] <= saraykan_area['max_lat']) &
                 (df['longitude'] >= saraykan_area['min_lon']) &
                 (df['longitude'] <= saraykan_area['max_lon'])]

# Обнаружение аномалий
threshold = 2  # Порог для определения аномалии
anomalies = df_filtered[(abs(df_filtered['water_level'] - df_filtered['water_level'].mean()) > threshold)]

# Создание карты
m = folium.Map(location=[saraykan_area['min_lat'], saraykan_area['min_lon']], zoom_start=12)

# Добавление маркеров для всех датчиков
marker_cluster = MarkerCluster()
for index, row in df_filtered.iterrows():
    marker_cluster.add_child(folium.Marker([row['latitude'], row['longitude']],
                                          popup=f"Sensor ID: {row['sensor_id']}, Water Level: {row['water_level']}"))
m.add_child(marker_cluster)

# Добавление маркеров для аномалий
for index, row in anomalies.iterrows():
    folium.Marker([row['latitude'], row['longitude']],
                  popup=f"Sensor ID: {row['sensor_id']}, Water Level: {row['water_level']} (Anomaly)",
                  icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("139.html")