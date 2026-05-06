import pandas as pd
import numpy as np
import folium
from datetime import timedelta

# Пример данных: временные ряды от датчиков на реках Лепсы и Киши Осек
data = {
    'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='H'),
    'sensor_id': ['Lepsa_1'] * 50 + ['Kishi_Oska_1'] * 50,
    'value': np.random.rand(100) * 100
}

# Создание DataFrame
df = pd.DataFrame(data)

# Имитация пропусков данных для демонстрации
np.random.seed(42)
missing_indices = np.random.choice(df.index, size=15, replace=False)
df.loc[missing_indices, 'value'] = np.nan

# Преобразование столбца timestamp в datetime формат
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Группировка данных по датчикам и проверка пропусков
grouped = df.groupby('sensor_id')
missing_periods = {}

for sensor, group in grouped:
    # Определение периодов отсутствия сигнала
    group.sort_values(by='timestamp', inplace=True)
    group['time_diff'] = group['timestamp'].diff()
    
    missing_intervals = []
    start_missing = None
    
    for i, row in group.iterrows():
        if pd.isna(row['value']):
            if start_missing is None:
                start_missing = row['timestamp']
        else:
            if start_missing is not None:
                end_missing = row['timestamp'] - timedelta(hours=1)
                missing_intervals.append((start_missing, end_missing))
                start_missing = None
    
    # Добавление последнего интервала пропуска, если он существует
    if start_missing is not None:
        missing_intervals.append((start_missing, group.iloc[-1]['timestamp']))
    
    missing_periods[sensor] = missing_intervals

# Координаты датчиков (примерные)
sensor_locations = {
    'Lepsa_1': [56.298347, 40.514772],
    'Kishi_Oska_1': [56.300000, 40.520000]
}

# Создание карты
m = folium.Map(location=[56.300000, 40.515000], zoom_start=13)

for sensor, intervals in missing_periods.items():
    lat, lon = sensor_locations[sensor]
    
    # Добавление маркера для датчика
    folium.Marker([lat, lon], popup=f"Датчик: {sensor}").add_to(m)
    
    for start, end in intervals:
        # Добавление полилиний для периодов отсутствия сигнала
        folium.PolyLine(
            locations=[[lat, lon], [lat + 0.001 * (np.random.rand() - 0.5), lon + 0.001 * (np.random.rand() - 0.5)]],
            color='red',
            popup=f"Пропуск с {start} по {end}"
        ).add_to(m)

# Сохранение карты
m.save("149.html")