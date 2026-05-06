import pandas as pd
import folium

# Загрузка данных (пример с CSV)
data = pd.read_csv('osek_river_sensors.csv')

# Предположим, что данные имеют следующие столбцы: 'latitude', 'longitude', 'sensor_id', 'status'
# Где 'status' может быть 'normal', 'warning', 'critical'

# Проверка данных на наличие пропущенных значений
print(data.isnull().sum())

# Анализ состояния датчиков
data['is_faulty'] = data['status'].apply(lambda x: True if x in ['warning', 'critical'] else False)

# Создание карты
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)

# Добавление маркеров на карте
for index, row in data.iterrows():
    color = 'green' if not row['is_faulty'] else 'red'
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Sensor ID: {row['sensor_id']}<br>Status: {row['status']}",
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("68.html")

print("Карта сохранена как 68.html")