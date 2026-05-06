import pandas as pd
import numpy as np
import folium
from datetime import datetime, timedelta

# 1. Генерация синтетических данных для реки Киши Осек
# В реальном сценарии здесь будет загрузка из БД или API
np.random.seed(42)

sensors_info = {
    'sensor_id': ['S1', 'S2', 'S3', 'S4', 'S5'],
    'lat': [42.123, 42.150, 42.180, 42.210, 42.250],
    'lon': [71.450, 71.470, 71.500, 71.530, 71.580],
    'name': ['Верхний пост', 'Пост А', 'Пост Б', 'Средний пост', 'Нижний пост']
}

df_sensors = pd.DataFrame(sensors_info)

# Создаем временные ряды за последние 24 часа (интервал 1 час)
timestamps = pd.date_range(start=datetime.now() - timedelta(days=1), periods=24, freq='H')
data_list = []

for _, sensor in df_sensors.iterrows():
    sid = sensor['sensor_id']
    for ts in timestamps:
        # Базовое значение с шумом
        val = 10.0 + np.random.normal(0, 0.5)
        
        # Искусственно создаем сбои для демонстрации
        if sid == 'S2' and ts.hour > 12: 
            val = np.nan  # Сбой: Пропуск данных (Data Gap)
        elif sid == 'S3': 
            val = 10.5  # Сбой: Замирание сигнала (Frozen Signal)
        elif sid == 'S5' and ts.hour == 10: 
            val = 99.9  # Сбой: Аномальный скачок (Outlier)
        else:
            val = val
            
        data_list.append({'sensor_id': sid, 'timestamp': ts, 'value': val})

df_measurements = pd.DataFrame(data_list)

# 2. Функция анализа сбоев
def analyze_equipment(measurements, sensors_meta):
    results = []
    
    for sid in sensors_meta['sensor_id']:
        sensor_data = measurements[measurements['sensor_id'] == sid].sort_values('timestamp')
        vals = sensor_data['value']
        
        status = "OK"
        issue = "Нет проблем"
        
        # Проверка на пропуски (NaN)
        if vals.isnull().any():
            status = "FAIL"
            issue = "Пропуск данных (NaN)"
        
        # Проверка на замирание (стандартное отклонение близко к 0)
        elif vals.std() < 0.01:
            status = "FAIL"
            issue = "Замирание сигнала (Frozen)"
            
        # Проверка на аномалии (Z-score > 3)
        elif (vals - vals.mean()).abs().max() > 3 * vals.std():
            status = "FAIL"
            issue = "Аномальный скачок значения"
            
        results.append({'sensor_id': sid, 'status': status, 'issue': issue})
        
    return pd.DataFrame(results)

# Выполняем анализ
analysis_df = analyze_equipment(df_measurements, df_sensors)
final_df = df_sensors.merge(analysis_df, on='sensor_id')

# 3. Визуализация на карте
# Центрируем карту по средним координатам реки
m = folium.Map(location=[final_df['lat'].mean(), final_df['lon'].mean()], 
               zoom_start=11, 
               tiles='CartoDB positron')

for _, row in final_df.iterrows():
    color = 'green' if row['status'] == 'OK' else 'red'
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=f"Датчик: {row['name']} ({row['sensor_id']})<br>Статус: {row['status']}<br>Проблема: {row['issue']}",
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# Сохранение результата
m.save("142.html")

print("Анализ завершен. Карта сохранена в файл 142.html")
print(final_df[['sensor_id', 'name', 'status', 'issue']])