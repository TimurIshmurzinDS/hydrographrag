import pandas as pd
import folium

# Загрузка данных
koktal_data = pd.read_csv('koktal_sensors.csv')
aksu_data = pd.read_csv('aksu_sensors.csv')

# Пример структуры данных:
# koktal_data: {'latitude', 'longitude', 'status'}
# aksu_data: {'latitude', 'longitude', 'status'}

# Создание карт
m_koktal = folium.Map(location=[koktal_data['latitude'].mean(), koktal_data['longitude'].mean()], zoom_start=10)
m_aksu = folium.Map(location=[aksu_data['latitude'].mean(), aksu_data['longitude'].mean()], zoom_start=10)

# Функция для добавления маркеров на карту
def add_markers(data, map_obj):
    for index, row in data.iterrows():
        if row['status'] == 'active':
            folium.Marker([row['latitude'], row['longitude']], 
                          popup=f"Koktal Sensor {index}: Active", 
                          icon=folium.Icon(color='green')).add_to(map_obj)
        else:
            folium.Marker([row['latitude'], row['longitude']], 
                          popup=f"Koktal Sensor {index}: Inactive", 
                          icon=folium.Icon(color='red')).add_to(map_obj)

# Добавление маркеров на карты
add_markers(koktal_data, m_koktal)
add_markers(aksu_data, m_aksu)

# Сохранение карт
m_koktal.save("koktal_sensors_map.html")
m_aksu.save("aksu_sensors_map.html")

print("Карты успешно сохранены как koktal_sensors_map.html и aksu_sensors_map.html")