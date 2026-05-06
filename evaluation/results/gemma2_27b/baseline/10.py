import folium
import pandas as pd

# Загрузка данных о датчиках
# Предполагаем, что данные хранятся в CSV файле с колонками 'id', 'latitude', 'longitude', 'status'
sensors = pd.read_csv("sensors_talgar.csv")

# Создание карты
m = folium.Map(location=[43.25, 77.0], zoom_start=12)  # Примерные координаты реки Talgar

# Добавление датчиков на карту
for index, row in sensors.iterrows():
    if row['status'] == 'working':
        color = 'green'
    else:
        color = 'red'
    folium.Marker(location=[row['latitude'], row['longitude']], 
                  popup=f"Датчик {row['id']}: {row['status']}",
                  icon=folium.Icon(color=color)).add_to(m)

# Сохранение карты
m.save("10.html")