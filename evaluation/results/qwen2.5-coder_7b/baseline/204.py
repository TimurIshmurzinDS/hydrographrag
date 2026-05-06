import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка данных (пример)
data_byzhy = pd.read_csv('byzhy_data.csv', parse_dates=['date'])
data_urzhar = pd.read_csv('urzhar_data.csv', parse_dates=['date'])

# Предварительный анализ
print("Предварительный анализ данных Byzhy River:")
print(data_byzhy.info())
print(data_byzhy.describe())

print("\nПредварительный анализ данных Urzhar River:")
print(data_urzhar.info())
print(data_urzhar.describe())

# Визуализация временных рядов
plt.figure(figsize=(12, 6))
plt.plot(data_byzhy['date'], data_byzhy['flow'], label='Byzhy River')
plt.plot(data_urzhar['date'], data_urzhar['flow'], label='Urzhar River')
plt.xlabel('Дата')
plt.ylabel('Сток (м³/с)')
plt.title('Временные ряды стока рек Byzhy и Urzhar')
plt.legend()
plt.show()

# Анализ статистических характеристик
print("\nСтатистические характеристики Byzhy River:")
print(data_byzhy['flow'].describe())

print("\nСтатистические характеристики Urzhar River:")
print(data_urzhar['flow'].describe())

# Сравнение сезонных изменений (пример с использованием библиотеки pandas)
data_byzhy['month'] = data_byzhy['date'].dt.month
data_urzhar['month'] = data_urzhar['date'].dt.month

seasonal_data_byzhy = data_byzhy.groupby('month')['flow'].mean()
seasonal_data_urzhar = data_urzhar.groupby('month')['flow'].mean()

plt.figure(figsize=(12, 6))
plt.plot(seasonal_data_byzhy.index, seasonal_data_byzhy.values, label='Byzhy River')
plt.plot(seasonal_data_urzhar.index, seasonal_data_urzhar.values, label='Urzhar River')
plt.xlabel('Месяц')
plt.ylabel('Средний сток (м³/с)')
plt.title('Сезонные изменения стока рек Byzhy и Urzhar')
plt.legend()
plt.show()

# Анализ корреляции
correlation = data_byzhy['flow'].corr(data_urzhar['flow'])
print(f"\nКорреляция между данными стока двух рек: {correlation}")

# Визуализация на карте (пример)
m = folium.Map(location=[data_byzhy['latitude'].mean(), data_byzhy['longitude'].mean()], zoom_start=10)

byzhy_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [data_byzhy.iloc[i]['longitude'], data_byzhy.iloc[i]['latitude']]
            },
            "properties": {
                "time": data_byzhy.iloc[i]['date'].strftime('%Y-%m-%dT%H:%M:%SZ'),
                "value": data_byzhy.iloc[i]['flow']
            }
        } for i in range(len(data_byzhy))
    ]
}

urzhar_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [data_urzhar.iloc[i]['longitude'], data_urzhar.iloc[i]['latitude']]
            },
            "properties": {
                "time": data_urzhar.iloc[i]['date'].strftime('%Y-%m-%dT%H:%M:%SZ'),
                "value": data_urzhar.iloc[i]['flow']
            }
        } for i in range(len(data_urzhar))
    ]
}

TimestampedGeoJson(byzhy_geojson, period="PT1H", add_last_point=True).add_to(m)
TimestampedGeoJson(urzhar_geojson, period="PT1H", add_last_point=True).add_to(m)

m.save("204.html")