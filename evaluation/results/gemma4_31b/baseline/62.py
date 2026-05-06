import pandas as pd
import folium
from datetime import datetime, timedelta

# 1. Симуляция данных мониторинга реки Шарын
# В реальном сценарии здесь был бы запрос к API или SQL базе данных
data = {
    'station_id': ['SH-01', 'SH-02', 'SH-03', 'SH-04', 'SH-05', 'SH-06'],
    'name': ['Верхний Шарын', 'Средний Шарын-1', 'Средний Шарын-2', 'Каньон-Вход', 'Каньон-Центр', 'Нижний Шарын'],
    'lat': [43.8521, 43.6123, 43.4567, 43.3210, 43.2105, 43.0543],
    'lon': [79.1234, 79.3456, 79.5678, 79.7890, 79.9123, 80.1234],
    'status': ['online', 'offline', 'online', 'offline', 'online', 'offline'],
    'last_update': [
        datetime.now(), 
        datetime.now() - timedelta(hours=5), 
        datetime.now(), 
        datetime.now() - timedelta(hours=12), 
        datetime.now(), 
        datetime.now() - timedelta(days=1)
    ]
}

df = pd.DataFrame(data)

# 2. Логика определения постов, не передающих данные
# Критерий: статус 'offline' или данные старше 1 часа
threshold_time = datetime.now() - timedelta(hours=1)
df['is_silent'] = (df['status'] == 'offline') | (df['last_update'] < threshold_time)

# Список постов, которые не передают данные
silent_stations = df[df['is_silent'] == True]

print("Посты, не передающие данные:")
print(silent_stations[['station_id', 'name', 'last_update']])

# 3. Визуализация на карте
# Центрируем карту на среднем значении координат реки Шарын
map_center = [df['lat'].mean(), df['lon'].mean()]
m = folium.Map(location=map_center, zoom_start=7, tiles='OpenStreetMap')

# Добавляем маркеры для всех станций
for index, row in df.iterrows():
    color = 'red' if row['is_silent'] else 'green'
    status_text = 'НЕ ПЕРЕДАЕТ ДАННЫЕ' if row['is_silent'] else 'Активен'
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=f"Пост: {row['name']}<br>ID: {row['station_id']}<br>Статус: {status_text}<br>Обновление: {row['last_update'].strftime('%Y-%m-%d %H:%M')}",
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# Сохранение карты
m.save("62.html")
print("\nКарта сохранена в файл 62.html")