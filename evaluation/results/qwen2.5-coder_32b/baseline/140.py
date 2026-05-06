import pandas as pd
import numpy as np
import folium

# Предположим, что у нас есть данные о датчиках и их параметрах связи
# Пример данных (в реальности данные могут быть загружены из файла или базы данных)
data = {
    'sensor_id': [1, 2, 3, 4, 5],
    'river': ['Токыраун', 'Токыраун', 'Аягоз', 'Аягоз', 'Аягоз'],
    'latitude': [42.8746, 42.8910, 43.0500, 43.0600, 43.0700],
    'longitude': [74.6120, 74.6300, 74.8900, 74.9000, 74.9100],
    'signal_quality_mean': [85, 90, 75, 80, 85],  # Среднее качество сигнала
    'signal_quality_std': [3, 2, 5, 4, 3]       # Стандартное отклонение качества сигнала
}

# Создаем DataFrame из данных
df = pd.DataFrame(data)

# Вычисляем метрику стабильности связи (например, обратно пропорциональная величина стандартного отклонения)
df['stability'] = 1 / df['signal_quality_std']

# Нормализуем значения стабильности для визуализации
df['stability_normalized'] = (df['stability'] - df['stability'].min()) / (df['stability'].max() - df['stability'].min())

# Создаем карту с использованием folium
m = folium.Map(location=[42.95, 74.80], zoom_start=10)

# Добавляем маркеры на карту для каждого датчика
for _, row in df.iterrows():
    color = 'green' if row['stability_normalized'] > 0.66 else ('orange' if row['stability_normalized'] > 0.33 else 'red')
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=10,
        popup=f"Датчик {row['sensor_id']} на реке {row['river']}\nСреднее качество сигнала: {row['signal_quality_mean']}",
        color=color,
        fill=True,
        fill_color=color
    ).add_to(m)

# Сохраняем карту в HTML-файл
m.save("140.html")