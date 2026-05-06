import pandas as pd
import folium
import random
from datetime import datetime, timedelta

# 1. Генерация синтетических данных для станций мониторинга
def generate_river_data():
    # Приблизительные координаты для рек в Казахстане
    # Tentek River (примерные координаты)
    tentek_coords = [[48.5, 72.0], [48.6, 72.2], [48.7, 72.4], [48.8, 72.6], [48.9, 72.8]]
    # Sharyn River (примерные координаты)
    sharyn_coords = [[44.2, 78.5], [44.3, 78.7], [44.4, 78.9], [44.5, 79.1], [44.6, 79.3]]
    
    statuses = ['Online', 'Offline', 'Warning']
    data = []
    
    # Создаем станции для Tentek
    for i, coord in enumerate(tentek_coords):
        data.append({
            'station_id': f'TENT_{i+1}',
            'river': 'Tentek River',
            'lat': coord[0],
            'lon': coord[1],
            'status': random.choices(statuses, weights=[0.7, 0.2, 0.1])[0],
            'last_update': (datetime.now() - timedelta(hours=random.randint(0, 48))).strftime('%Y-%m-%d %H:%M')
        })
        
    # Создаем станции для Sharyn
    for i, coord in enumerate(sharyn_coords):
        data.append({
            'station_id': f'SHAR_{i+1}',
            'river': 'Sharyn River',
            'lat': coord[0],
            'lon': coord[1],
            'status': random.choices(statuses, weights=[0.4, 0.4, 0.2])[0],
            'last_update': (datetime.now() - timedelta(hours=random.randint(0, 48))).strftime('%Y-%m-%d %H:%M')
        })
        
    return pd.DataFrame(data)

# 2. Анализ и сравнение
def analyze_transmission(df):
    summary = df.groupby('river')['status'].value_counts(normalize=True).unstack().fillna(0) * 100
    print("--- Сравнение статуса передачи данных (%) ---")
    print(summary)
    print("\n")
    
    # Определяем, какая река имеет лучший статус Online
    tentek_online = summary.loc['Tentek River', 'Online'] if 'Online' in summary.columns else 0
    sharyn_online = summary.loc['Sharyn River', 'Online'] if 'Online' in summary.columns else 0
    
    if tentek_online > sharyn_online:
        print(f"Статус передачи данных на Tentek River лучше ({tentek_online:.2f}% vs {sharyn_online:.2f}%)")
    else:
        print(f"Статус передачи данных на Sharyn River лучше ({sharyn_online:.2f}% vs {tentek_online:.2f}%)")

# 3. Визуализация
def create_map(df):
    # Центрируем карту между двумя регионами
    m = folium.Map(location=[46.5, 75.0], zoom_start=5)
    
    # Цветовая схема для статусов
    color_map = {
        'Online': 'green',
        'Offline': 'red',
        'Warning': 'orange'
    }
    
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=8,
            popup=f"Station: {row['station_id']}<br>River: {row['river']}<br>Status: {row['status']}<br>Last Update: {row['last_update']}",
            color=color_map[row['status']],
            fill=True,
            fill_color=color_map[row['status']],
            fill_opacity=0.7
        ).add_to(m)
    
    m.save("75.html")

# Основной запуск
if __name__ == "__main__":
    df_stations = generate_river_data()
    analyze_transmission(df_stations)
    create_map(df_stations)
    print("\nКарта сохранена в файл 75.html")