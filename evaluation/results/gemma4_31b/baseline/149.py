import pandas as pd
import numpy as np
import folium
from datetime import timedelta

# 1. Симуляция данных (так как реальный файл не предоставлен)
def generate_mock_data():
    np.random.seed(42)
    rivers = {
        "Лепсы": {"coords": (55.1, 128.5), "sensors": 3},
        "Киши Осек": {"coords": (55.2, 128.7), "sensors": 3}
    }
    
    data = []
    # Создаем временную сетку (каждые 15 минут за 2 дня)
    time_range = pd.date_range(start="2023-10-01", end="2023-10-03", freq="15T")
    
    for river_name, info in rivers.items():
        for s_id in range(info["sensors"]):
            sensor_name = f"Sensor_{river_name}_{s_id}"
            # Генерируем случайные координаты вокруг центра реки
            lat = info["coords"][0] + np.random.uniform(-0.1, 0.1)
            lon = info["coords"][1] + np.random.uniform(-0.1, 0.1)
            
            # Создаем данные с искусственными пропусками
            for ts in time_range:
                # Имитируем потерю сигнала: с вероятностью 5% пропускаем запись
                if np.random.random() > 0.05:
                    data.append([sensor_name, river_name, ts, lat, lon, np.random.uniform(10, 20)])
                    
    return pd.DataFrame(data, columns=["sensor_id", "river", "timestamp", "lat", "lon", "value"])

# Загрузка данных
df = generate_mock_data()

# 2. Анализ отсутствия сигнала
# Определяем порог: если разрыв > 30 минут, считаем это отсутствием сигнала
THRESHOLD = timedelta(minutes=30)

# Сортировка
df = df.sort_values(by=["sensor_id", "timestamp"])

# Вычисляем разницу во времени между соседними записями для каждого датчика
df['time_diff'] = df.groupby('sensor_id')['timestamp'].diff()

# Находим строки, где зафиксирован разрыв
gaps = df[df['time_diff'] > THRESHOLD].copy()

# Считаем количество разрывов и общую длительность для каждого датчика
gap_summary = gaps.groupby('sensor_id').agg({
    'time_diff': ['count', 'sum']
}).reset_index()
gap_summary.columns = ['sensor_id', 'gap_count', 'total_gap_duration']

# 3. Визуализация на карте
# Получаем уникальный список датчиков и их координат
sensors_info = df[['sensor_id', 'river', 'lat', 'lon']].drop_duplicates('sensor_id')
sensors_info = sensors_info.merge(gap_summary, on='sensor_id', how='left').fillna(0)

# Создание карты
m = folium.Map(location=[55.15, 128.6], zoom_start=9, tiles="CartoDB positron")

for _, row in sensors_info.iterrows():
    # Определяем цвет: красный если есть разрывы, зеленый если нет
    color = 'red' if row['gap_count'] > 0 else 'green'
    
    # Формируем текст для всплывающего окна
    popup_text = (
        f"<b>Датчик:</b> {row['sensor_id']}<br>"
        f"<b>Река:</b> {row['river']}<br>"
        f"<b>Разрывов:</b> {int(row['gap_count'])}<br>"
        f"<b>Общее время простоя:</b> {row['total_gap_duration']}"
    )
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=7,
        popup=folium.Popup(popup_text, max_width=300),
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# Сохранение карты
m.save("149.html")

print("Анализ завершен. Карта сохранена в файл 149.html")
print(f"Обнаружено проблемных датчиков: {len(gap_summary)}")