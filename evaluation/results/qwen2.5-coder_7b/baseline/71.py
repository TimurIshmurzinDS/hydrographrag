import pandas as pd
import folium

# Пример данных о местоположении и статусе сенсоров
data = {
    'sensor_id': [1, 2, 3, 4],
    'latitude': [50.123, 50.124, 50.125, 50.126],
    'longitude': [30.123, 30.124, 30.125, 30.126],
    'status': ['active', 'inactive', 'active', 'unknown']
}

# Создание DataFrame
df = pd.DataFrame(data)

# Фильтрация данных для сенсоров на реке Byzhy River
byzhy_sensors = df[df['latitude'].between(50.123, 50.126) & 
                    df['longitude'].between(30.123, 30.126)]

# Создание карты
m = folium.Map(location=[50.1245, 30.1245], zoom_start=15)

# Добавление маркеров сенсоров на карте
for index, row in byzhy_sensors.iterrows():
    if row['status'] == 'active':
        folium.Marker([row['latitude'], row['longitude']], 
                      popup=f"Sensor {row['sensor_id']} - Active", 
                      icon=folium.Icon(color='green')).add_to(m)
    elif row['status'] == 'inactive':
        folium.Marker([row['latitude'], row['longitude']], 
                      popup=f"Sensor {row['sensor_id']} - Inactive", 
                      icon=folium.Icon(color='red')).add_to(m)
    else:
        folium.Marker([row['latitude'], row['longitude']], 
                      popup=f"Sensor {row['sensor_id']} - Unknown Status", 
                      icon=folium.Icon(color='orange')).add_to(m)

# Сохранение карты
m.save("71.html")