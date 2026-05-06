import pandas as pd
import folium

# Шаг 1: Сбор данных (предположим, что данные хранятся в CSV файле)
data = pd.read_csv('sensor_data.csv')

# Пример структуры данных:
# timestamp, sensor_id, temperature, flow_rate, status
# 2023-10-01 12:00:00, S1, 15.2, 120.5, OK
# 2023-10-01 12:05:00, S1, 14.8, 119.7, OK

# Шаг 2: Предварительная обработка данных
data['timestamp'] = pd.to_datetime(data['timestamp'])
latest_data = data.sort_values(by='timestamp', ascending=False).drop_duplicates(subset='sensor_id').head(1)

# Проверка на наличие пропусков или аномалий
if latest_data.isnull().values.any():
    print("В данных есть пропущенные значения.")
else:
    print("Данные полные.")

# Шаг 3: Анализ состояния датчика
sensor_status = latest_data['status'].iloc[0]
if sensor_status == 'OK':
    print("Состояние датчика нормальное.")
else:
    print(f"Проблема с датчиком: {sensor_status}")

# Шаг 4: Визуализация результатов
# Координаты реки Улкен Алматы Ривер (примерные)
river_coordinates = [42.874365, 74.590113]

# Создание карты
m = folium.Map(location=river_coordinates, zoom_start=12)

# Добавление маркера для датчика
sensor_location = [42.875000, 74.591000]  # Примерные координаты датчика
folium.Marker(
    location=sensor_location,
    popup=f"Состояние датчика: {sensor_status}",
    icon=folium.Icon(color='green' if sensor_status == 'OK' else 'red')
).add_to(m)

# Сохранение карты в HTML файл
m.save("8.html")