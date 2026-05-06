import pandas as pd
from folium import Map, Marker
import numpy as np

# Загрузка данных о показаниях сенсоров и метеоусловиях
sensors_data = pd.read_csv('sensors_data.csv')
weather_data = pd.read_csv('weather_data.csv')

# Подготовка данных к анализу: очистка, преобразование типов и объединение таблиц
data = pd.merge(sensors_data, weather_data, on='date')
data.dropna(inplace=True)  # Удаление строк с пропущенными значениями

# Анализ показаний сенсоров для выявления аномалий
def detect_anomalies(data):
    z_scores = np.abs((data['value'] - data['value'].mean()) / data['value'].std())
    anomalies = data[z_scores > 2]
    return anomalies

anomalies = detect_anomalies(data)

# Визуализация результатов на карте
m = Map(location=[55.7558, 37.6173], zoom_start=10)
for index, row in anomalies.iterrows():
    Marker([row['latitude'], row['longitude']], popup=f'Аномалия обнаружена в {row["date"]}').add_to(m)

# Сохранение карты
m.save("74.html")