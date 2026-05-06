import pandas as pd
import numpy as np
import folium
from datetime import datetime, timedelta

# 1. Симуляция данных сенсоров на реке Tentek River
np.random.seed(42)

# Координаты примерного расположения сенсоров вдоль реки (условно)
sensors_coords = {
    'Sensor_1': [48.50, 82.10],
    'Sensor_2': [48.45, 82.25],
    'Sensor_3': [48.40, 82.40],
    'Sensor_4': [48.35, 82.55],
    'Sensor_5': [48.30, 82.70]
}

# Создаем временной ряд (последние 24 часа, замеры каждые 15 минут)
time_index = pd.date_range(start='2023-10-01', periods=96, freq='15T')
data_list = []

for s_id, coords in sensors_coords.items():
    # Базовый сигнал: синусоида + шум
    base_signal = 2.0 + 0.5 * np.sin(np.linspace(0, 2 * np.pi, 96)) + np.random.normal(0, 0.1, 96)
    
    # Вносим искусственные ошибки
    if s_id == 'Sensor_2': # Выброс
        base_signal[20] = 15.0 
    elif s_id == 'Sensor_3': # Замирание (stuck)
        base_signal[40:80] = 2.1
    elif s_id == 'Sensor_4': # Пропуски (NaN)
        base_signal[10:30] = np.nan
        
    for t, val in zip(time_index, base_signal):
        data_list.append({'sensor_id': s_id, 'timestamp': t, 'value': val})

df = pd.DataFrame(data_list)

# 2. Функция анализа ошибок
def analyze_sensors(df):
    results = {}
    unique_sensors = df['sensor_id'].unique()
    
    for s_id in unique_sensors:
        s_data = df[df['sensor_id'] == s_id]['value']
        errors = []
        
        # Проверка на пропуски
        if s_data.isna().sum() > 0:
            errors.append(f"Missing data ({s_data.isna().sum()} gaps)")
            
        # Проверка на выбросы (Z-score)
        mean = s_data.mean()
        std = s_data.std()
        if std > 0:
            z_scores = np.abs((s_data - mean) / std)
            if z_scores.max() > 3:
                errors.append("Outliers detected")
        
        # Проверка на замирание (стандартное отклонение в окне)
        # Если данные есть, но они абсолютно идентичны на протяжении части периода
        if len(s_data) > 1 and s_data.std() < 0.01:
            errors.append("Sensor stuck (no variance)")
        elif len(s_data) > 1:
            # Проверка на локальное замирание (например, 10 замеров подряд одинаковы)
            diffs = s_data.diff().fillna(0)
            if (diffs == 0).sum() > 20: # упрощенный порог
                errors.append("Local signal freeze")

        results[s_id] = {
            'status': 'Error' if errors else 'OK',
            'details': "; ".join(errors) if errors else 'Working normally'
        }
    return results

# Выполняем анализ
sensor_status = analyze_sensors(df)

# 3. Визуализация на карте
# Центр карты (среднее по координатам)
m = folium.Map(location=[48.4, 82.4], zoom_start=9, tiles='OpenStreetMap')

for s_id, coords in sensors_coords.items():
    status = sensor_status[s_id]['status']
    details = sensor_status[s_id]['details']
    
    color = 'red' if status == 'Error' else 'green'
    
    folium.Marker(
        location=coords,
        popup=f"<b>{s_id}</b><br>Status: {status}<br>Details: {details}",
        tooltip=f"{s_id}: {status}",
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("64.html")

print("Analysis complete. Map saved as 64.html")
# Вывод результатов в консоль для проверки
for s, res in sensor_status.items():
    print(f"{s}: {res['status']} -> {res['details']}")