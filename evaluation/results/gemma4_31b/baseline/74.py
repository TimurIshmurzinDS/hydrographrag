import pandas as pd
import numpy as np
import folium
from scipy import stats

# 1. Генерация синтетических данных для реки Prokhodnaya River
# Создаем координаты, имитирующие течение реки
river_coords = [
    [55.75, 37.61], [55.76, 37.63], [55.78, 37.65], 
    [55.80, 37.68], [55.82, 37.70], [55.85, 37.72]
]

# Создаем данные сенсоров (один сенсор в каждой точке)
np.random.seed(42)
sensors_data = {
    'sensor_id': [f'S_{i}' for i in range(len(river_coords))],
    'lat': [c[0] for c in river_coords],
    'lon': [c[1] for c in river_coords],
    'value': [12.5, 13.1, 12.8, 45.2, 12.9, 13.0] # 45.2 - явная аномалия
}

df = pd.DataFrame(sensors_data)

# 2. Поиск аномалий с помощью Z-score
# Вычисляем Z-score для колонки 'value'
df['z_score'] = np.abs(stats.zscore(df['value']))

# Определяем порог аномалии (например, Z > 1.5 для демонстрации на малом объеме данных)
threshold = 1.5
df['is_anomaly'] = df['z_score'] > threshold

# 3. Визуализация на карте
# Создаем карту, центрированную по средним координатам
m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=12, tiles='CartoDB positron')

# Рисуем линию реки
folium.PolyLine(river_coords, color="blue", weight=5, opacity=0.7, tooltip="Prokhodnaya River").add_to(m)

# Добавляем маркеры сенсоров
for index, row in df.iterrows():
    color = 'red' if row['is_anomaly'] else 'green'
    status = 'ANOMALY' if row['is_anomaly'] else 'NORMAL'
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=f"Sensor: {row['sensor_id']}<br>Value: {row['value']}<br>Z-Score: {row['z_score']:.2f}<br>Status: {status}",
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# Сохранение карты
m.save("74.html")

print("Analysis complete. The map has been saved as 74.html.")
print(df[['sensor_id', 'value', 'z_score', 'is_anomaly']])