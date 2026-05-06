import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import folium

# Предположим, что у нас есть CSV файл с данными о гидропостах и их временных рядах расхода воды.
# Файл должен содержать столбцы: 'station_id', 'latitude', 'longitude', 'date', 'discharge'

# Загрузка данных
data = pd.read_csv('tokyraun_river_data.csv', parse_dates=['date'])

# Предварительная обработка данных
data.dropna(subset=['discharge'], inplace=True)

# Функция для поиска резких изменений в временных рядах
def find_sudden_increases(series, threshold=0.5):
    peaks, _ = find_peaks(series, height=np.mean(series) + np.std(series) * threshold)
    return peaks

# Анализ данных для каждого гидропоста
sudden_increase_stations = []
for station_id, group in data.groupby('station_id'):
    group.sort_values(by='date', inplace=True)
    discharge_series = group['discharge'].values
    peaks = find_sudden_increases(discharge_series)
    if len(peaks) > 0:
        sudden_increase_stations.append(station_id)

# Визуализация результатов на карте с использованием folium
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)

for station_id, group in data.groupby('station_id'):
    lat = group['latitude'].iloc[0]
    lon = group['longitude'].iloc[0]
    if station_id in sudden_increase_stations:
        folium.Marker([lat, lon], popup=f'Гидропост {station_id} - Резкий рост расхода воды', icon=folium.Icon(color='red')).add_to(m)
    else:
        folium.Marker([lat, lon], popup=f'Гидропост {station_id}', icon=folium.Icon(color='blue')).add_to(m)

# Сохранение карты в файл
m.save("84.html")