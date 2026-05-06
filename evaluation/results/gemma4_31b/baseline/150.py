import pandas as pd
import numpy as np
import folium
from datetime import datetime, timedelta

# 1. Симуляция данных
def generate_sensor_data():
    np.random.seed(42)
    # Координаты датчиков (приблизительные для рек Или и Каратал)
    sensors = {
        'Ili_1': [43.2, 79.1], 'Ili_2': [43.5, 78.5], 'Ili_3': [43.8, 77.8],
        'Karatal_1': [43.6, 77.2], 'Karatal_2': [43.4, 77.5], 'Karatal_3': [43.2, 77.8]
    }
    
    data_list = []
    start_date = datetime(2023, 1, 1)
    
    for sensor_id, coords in sensors.items():
        # Базовый уровень воды
        base_level = np.random.uniform(2.0, 5.0)
        
        for i in range(100):  # 100 замеров на датчик
            timestamp = start_date + timedelta(hours=i*6)
            
            # Добавляем шум и сезонность
            noise = np.random.normal(0, 0.1)
            level = base_level + np.sin(i/10) + noise
            
            # Искусственно создаем нестабильность для некоторых датчиков
            if sensor_id == 'Ili_2' and i % 10 == 0:
                level += np.random.uniform(2, 5)  # Резкие скачки
            if sensor_id == 'Karatal_3' and i % 5 == 0:
                level = np.nan  # Пропуски данных
                
            data_list.append([sensor_id, coords[0], coords[1], timestamp, level])
            
    return pd.DataFrame(data_list, columns=['sensor_id', 'lat', 'lon', 'timestamp', 'water_level'])

# 2. Анализ стабильности
def analyze_stability(df):
    results = []
    sensors = df['sensor_id'].unique()
    
    for s in sensors:
        s_data = df[df['sensor_id'] == s]['water_level'].dropna()
        
        mean_val = s_data.mean()
        std_val = s_data.std()
        cv = (std_val / mean_val) if mean_val != 0 else 0
        
        # Считаем пропуски
        total_expected = len(df[df['sensor_id'] == s])
        missing_pct = (1 - (len(s_data) / total_expected)) * 100
        
        # Определение статуса
        if cv < 0.1 and missing_pct < 5:
            status = 'Stable'
            color = 'green'
        elif cv < 0.25 and missing_pct < 20:
            status = 'Suspicious'
            color = 'orange'
        else:
            status = 'Unstable'
            color = 'red'
            
        results.append({
            'sensor_id': s,
            'cv': cv,
            'missing_pct': missing_pct,
            'status': status,
            'color': color
        })
        
    return pd.DataFrame(results)

# --- Основной процесс ---

# Генерация данных
df_raw = generate_sensor_data()
# Анализ
df_stability = analyze_stability(df_raw)

# Объединение координат с результатами анализа
df_final = df_raw[['sensor_id', 'lat', 'lon']].drop_duplicates().merge(df_stability, on='sensor_id')

# 3. Визуализация на карте
m = folium.Map(location=[43.5, 78.0], zoom_start=7, tiles='CartoDB positron')

for _, row in df_final.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=f"Sensor: {row['sensor_id']}<br>Status: {row['status']}<br>CV: {row['cv']:.2%}<br>Missing: {row['missing_pct']:.1f}%",
        color=row['color'],
        fill=True,
        fill_color=row['color'],
        fill_opacity=0.7
    ).add_to(m)

# Сохранение карты
m.save("150.html")

print("Analysis complete. Map saved as 150.html")