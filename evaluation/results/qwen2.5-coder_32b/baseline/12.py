import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import folium

# Предполагаем, что у нас есть данные в CSV файле со столбцами: 'timestamp', 'sensor_value', 'latitude', 'longitude'
data = pd.read_csv('prokhodnaya_river_sensor_data.csv')

# Преобразуем timestamp в datetime формат
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Сортируем данные по времени
data.sort_values(by='timestamp', inplace=True)

# Предварительный анализ данных: проверка на пропуски и аномалии
print("Пропущенные значения:")
print(data.isnull().sum())

# Визуализация временных рядов
plt.figure(figsize=(14, 7))
plt.plot(data['timestamp'], data['sensor_value'], label='Значения сенсора')
plt.title('Временной ряд значений сенсора на реке Прокходная')
plt.xlabel('Время')
plt.ylabel('Значение сенсора')
plt.legend()
plt.grid(True)
plt.show()

# Статистический анализ: поиск выбросов
z_scores = stats.zscore(data['sensor_value'])
data['anomaly'] = z_scores > 3

# Визуализация аномалий на графике
plt.figure(figsize=(14, 7))
plt.plot(data['timestamp'], data['sensor_value'], label='Значения сенсора')
plt.scatter(data[data['anomaly']]['timestamp'], data[data['anomaly']]['sensor_value'], color='red', label='Аномалии')
plt.title('Временной ряд значений сенсора на реке Прокходная с аномалиями')
plt.xlabel('Время')
plt.ylabel('Значение сенсора')
plt.legend()
plt.grid(True)
plt.show()

# Создание интерактивной карты
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)

# Добавление маркеров для аномалий
for idx, row in data[data['anomaly']].iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Аномальное значение: {row['sensor_value']}<br>Время: {row['timestamp']}",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты
m.save("12.html")