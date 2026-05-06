import pandas as pd
import numpy as np
from folium import Map, Marker
from folium.plugins import HeatMap

# Загрузка данных
water_consumption = pd.read_csv('water_consumption.csv')
crop_yield = pd.read_csv('crop_yield.csv')

# Объединение данных по географическому координату
merged_data = pd.merge(water_consumption, crop_yield, on='location')

# Создание модели корреляции
correlation_model = merged_data['water_consumption'].corr(merged_data['crop_yield'])

print(f"Корреляция между расходом воды и урожайностью: {correlation_model}")

# Визуализация результатов на карте
m = Map(location=[55.7558, 37.6173], zoom_start=10)
HeatMap(data=merged_data[['water_consumption', 'crop_yield']].values.tolist(), radius=20).add_to(m)

# Добавление маркеров для каждого географического координата
for index, row in merged_data.iterrows():
    Marker(location=[row['latitude'], row['longitude']], popup=f"Расход воды: {row['water_consumption']}, Урожайность: {row['crop_yield']}").add_to(m)

# Сохранение карты в файл
m.save("185.html")