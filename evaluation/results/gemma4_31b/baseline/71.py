import folium
import pandas as pd

# 1. Симуляция данных о сенсорах
# В реальном сценарии здесь была бы загрузка из GeoJSON, PostGIS или API
data = {
    'sensor_id': ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
    'river': ['Byzhy River', 'Byzhy River', 'Byzhy River', 'Other River', 'Byzhy River', 'Other River'],
    'lat': [52.1234, 52.1345, 52.1456, 53.0000, 52.1567, 53.1000],
    'lon': [30.1111, 30.1222, 30.1333, 31.0000, 30.1444, 31.1000],
    'status': ['Active', 'Inactive', 'Active', 'Active', 'Active', 'Inactive']
}

df = pd.DataFrame(data)

def check_sensors_status(df, river_name):
    # 2. Фильтрация сенсоров по конкретной реке
    river_sensors = df[df['river'] == river_name]
    
    if river_sensors.empty:
        print(f"Сенсоры на реке {river_name} не найдены.")
        return None, None

    # 3. Проверка активности
    inactive_sensors = river_sensors[river_sensors['status'] != 'Active']
    
    if inactive_sensors.empty:
        print(f"Все сенсоры на реке {river_name} находятся в активном режиме.")
    else:
        print(f"ВНИМАНИЕ: На реке {river_name} обнаружены неактивные сенсоры!")
        print(inactive_sensors[['sensor_id', 'status']].to_string(index=False))
    
    return river_sensors, inactive_sensors

# Выполнение анализа
river_name = "Byzhy River"
byzhy_sensors, inactive_list = check_sensors_status(df, river_name)

if byzhy_sensors is not None:
    # 4. Визуализация на карте
    # Вычисляем центр карты по средним координатам сенсоров реки
    center_lat = byzhy_sensors['lat'].mean()
    center_lon = byzhy_sensors['lon'].mean()
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
    
    for _, row in byzhy_sensors.iterrows():
        # Цвет маркера: зеленый если Active, красный если нет
        color = 'green' if row['status'] == 'Active' else 'red'
        
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=f"Sensor: {row['sensor_id']}<br>Status: {row['status']}",
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(m)
    
    # 5. Сохранение карты
    m.save("71.html")
    print("Карта сохранена в файл 71.html")