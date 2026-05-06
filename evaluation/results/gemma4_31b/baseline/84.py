import pandas as pd
import numpy as np
import folium
from datetime import datetime

# 1. Симуляция данных (в реальном сценарии здесь будет загрузка из БД или CSV)
# Координаты реки Tokyraun (примерные значения для региона Якутии)
stations_data = {
    'station_id': ['HP_01', 'HP_02', 'HP_03', 'HP_04', 'HP_05'],
    'lat': [66.52, 66.45, 66.38, 66.30, 66.22],
    'lon': [132.10, 132.25, 132.40, 132.55, 132.70],
    'name': ['Верхний Токыраун', 'Средний-1', 'Средний-2', 'Нижний-1', 'Устьевой']
}

df_stations = pd.DataFrame(stations_data)

# Генерация синтетических временных рядов расхода воды (м3/с) за весну (март-май)
np.random.seed(42)
dates = pd.date_range(start="2023-03-01", end="2023-05-31", freq='D')
time_series_list = []

for s_id in df_stations['station_id']:
    # Создаем базовый тренд половодья (синусоида + шум)
    base = np.linspace(10, 100, len(dates)) 
    noise = np.random.normal(0, 5, len(dates))
    
    # Искусственно создаем "резкий рост" для некоторых постов
    spike = np.zeros(len(dates))
    if s_id in ['HP_02', 'HP_04']: # Эти посты будут "критическими"
        spike[40:45] = np.linspace(0, 150, 5) # Резкий скачок в апреле
        
    discharge = base + noise + spike
    for date, val in zip(dates, discharge):
        time_series_list.append({'station_id': s_id, 'date': date, 'discharge': val})

df_ts = pd.DataFrame(time_series_list)

# 2. Анализ резкого роста
def detect_sharp_increase(group):
    # Вычисляем разницу между соседними днями
    diff = group['discharge'].diff()
    # Порог: если рост за сутки > 40 м3/с (условный порог для примера)
    threshold = 40 
    max_growth = diff.max()
    is_sharp = max_growth > threshold
    return pd.Series({'max_growth': max_growth, 'is_sharp': is_sharp})

# Группируем по станциям и применяем функцию анализа
analysis_results = df_ts.groupby('station_id').apply(detect_sharp_increase).reset_index()

# Объединяем результаты с данными о координатах
final_df = pd.merge(df_stations, analysis_results, on='station_id')

# 3. Визуализация на карте
# Центр карты (примерно по реке Tokyraun)
m = folium.Map(location=[66.35, 132.40], zoom_start=7, tiles='OpenStreetMap')

for idx, row in final_df.iterrows():
    # Цвет: красный если резкий рост, зеленый если нет
    color = 'red' if row['is_sharp'] else 'green'
    
    popup_text = (
        f"Станция: {row['name']}<br>"
        f"ID: {row['station_id']}<br>"
        f"Макс. рост за сутки: {row['max_growth']:.2f} м3/с<br>"
        f"Статус: {'РЕЗКИЙ РОСТ' if row['is_sharp'] else 'Норма'}"
    )
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        popup=popup_text,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# Сохранение карты
m.save("84.html")

print("Анализ завершен. Результаты сохранены в файл 84.html")