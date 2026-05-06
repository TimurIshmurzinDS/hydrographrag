import pandas as pd
import folium
from datetime import datetime

# Пример данных о местоположении датчиков и их сигналы
data = {
    'sensor_id': ['S1', 'S2'],
    'latitude': [50.45, 50.46],
    'longitude': [30.50, 30.51],
    'signal_times': [
        [('2023-01-01 08:00', '2023-01-01 12:00'), ('2023-01-02 09:00', '2023-01-02 15:00')],
        [('2023-01-01 10:00', '2023-01-01 14:00'), ('2023-01-03 08:00', '2023-01-03 16:00')]
    ]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Функция для определения периодов отсутствия сигнала
def find_missing_periods(signal_times):
    all_periods = []
    for start, end in signal_times:
        all_periods.append((datetime.strptime(start, '%Y-%m-%d %H:%M'), datetime.strptime(end, '%Y-%m-%d %H:%M')))
    
    missing_periods = []
    current_time = all_periods[0][1]
    
    for period in all_periods[1:]:
        if period[0] > current_time:
            missing_periods.append((current_time, period[0]))
        current_time = max(current_time, period[1])
    
    return missing_periods

# Определение периодов отсутствия сигнала для каждого датчика
df['missing_periods'] = df['signal_times'].apply(find_missing_periods)

# Создание карты
m = folium.Map(location=[50.45, 30.50], zoom_start=12)

# Добавление маркеров с информацией о периодах отсутствия сигнала
for index, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Sensor ID: {row['sensor_id']}<br>Missing Periods: {', '.join([f'{start.strftime('%Y-%m-%d %H:%M')} - {end.strftime('%Y-%m-%d %H:%M')}' for start, end in row['missing_periods']])}",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты
m.save("149.html")