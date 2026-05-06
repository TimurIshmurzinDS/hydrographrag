import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster

def solve_spaceship_problem():
    # 1. Симуляция данных датчиков реки Батарейка
    # Предположим, река протекает в определенном регионе (координаты вокруг условной точки)
    np.random.seed(42)
    num_sensors = 15
    
    # Генерация координат вдоль воображаемой реки (линейная интерполяция с шумом)
    start_lat, start_lon = 55.75, 37.61
    lats = np.linspace(start_lat, start_lat + 0.1, num_sensors) + np.random.normal(0, 0.005, num_sensors)
    lons = np.linspace(start_lon, start_lon + 0.1, num_sensors) + np.random.normal(0, 0.005, num_sensors)
    
    # Параметры датчиков: уровень воды, скорость потока, содержание минералов (0-100)
    data = {
        'sensor_id': [f"SEN_{i}" for i in range(num_sensors)],
        'lat': lats,
        'lon': lons,
        'water_level': np.random.uniform(10, 100, num_sensors),
        'flow_rate': np.random.uniform(10, 100, num_sensors),
        'minerals': np.random.uniform(10, 100, num_sensors)
    }
    
    df = pd.DataFrame(data)
    
    # 2. Моделирование "строительного потенциала"
    # Веса: минералы важнее всего для корпуса, затем вода для охлаждения, затем поток
    w_water = 0.2
    w_flow = 0.3
    w_minerals = 0.5
    
    df['suitability_score'] = (df['water_level'] * w_water + 
                               df['flow_rate'] * w_flow + 
                               df['minerals'] * w_minerals)
    
    # Поиск оптимальной точки для строительства корабля
    best_site = df.loc[df['suitability_score'].idxmax()]
    
    # 3. Визуализация на карте
    # Создаем карту, центрированную на среднем значении координат
    m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=12, tiles='CartoDB dark_matter')
    
    # Рисуем линию реки (соединяем датчики)
    river_coords = df[['lat', 'lon']].values.tolist()
    folium.PolyLine(river_coords, color="blue", weight=3, opacity=0.7, tooltip="Batareyka River").add_to(m)
    
    # Добавляем датчики на карту
    sensor_cluster = MarkerCluster().add_to(m)
    for idx, row in df.iterrows():
        color = 'green' if row['suitability_score'] > 60 else 'orange' if row['suitability_score'] > 40 else 'red'
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=6,
            color=color,
            fill=True,
            fill_color=color,
            popup=f"Sensor: {row['sensor_id']}<br>Score: {row['suitability_score']:.2f}",
            tooltip=f"Sensor {row['sensor_id']}"
        ).add_to(sensor_cluster)
    
    # Добавляем маркер космического корабля
    folium.Marker(
        location=[best_site['lat'], best_site['lon']],
        popup=f"🚀 SPACE SHIP CONSTRUCTION SITE\nMax Score: {best_site['suitability_score']:.2f}",
        tooltip="Spaceship Site",
        icon=folium.Icon(color='purple', icon='rocket', prefix='fa')
    ).add_to(m)
    
    # Сохранение карты
    m.save("220.html")
    print("Modeling complete. The optimal site for the spaceship has been identified.")
    print(f"Best coordinates: {best_site['lat']:.4f}, {best_site['lon']:.4f}")

if __name__ == "__main__":
    solve_spaceship_problem()