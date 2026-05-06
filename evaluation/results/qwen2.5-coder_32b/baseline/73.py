import pandas as pd
import folium

# Предполагаемые данные о датчиках уровня воды для рек Осек и Коктал.
# В реальном сценарии эти данные должны быть получены из источника данных, например, API или базы данных.

data = {
    'river': ['Osek River', 'Osek River', 'Koktal River', 'Koktal River'],
    'sensor_id': [101, 102, 201, 202],
    'latitude': [54.321, 54.325, 56.789, 56.793],
    'longitude': [37.123, 37.127, 40.567, 40.571],
    'water_level': [150, 155, 120, 125],  # Уровень воды в сантиметрах
    'status': ['OK', 'OK', 'ERROR', 'OK']  # Состояние датчика: OK или ERROR
}

# Создание DataFrame из данных
df = pd.DataFrame(data)

# Проверка на наличие пропусков и аномалий
if df.isnull().values.any():
    print("В данных есть пропущенные значения.")
else:
    print("Пропущенных значений нет.")

# Анализ состояния датчиков
for index, row in df.iterrows():
    if row['status'] == 'ERROR':
        print(f"Датчик {row['sensor_id']} на реке {row['river']} не работает корректно.")
    else:
        print(f"Датчик {row['sensor_id']} на реке {row['river']} работает корректно. Уровень воды: {row['water_level']} см.")

# Создание интерактивной карты с помощью folium
m = folium.Map(location=[55.5, 38.5], zoom_start=6)

# Добавление маркеров на карту для каждого датчика
for index, row in df.iterrows():
    if row['status'] == 'OK':
        color = 'green'
    else:
        color = 'red'
    
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Река: {row['river']}<br>Датчик ID: {row['sensor_id']}<br>Уровень воды: {row['water_level']} см<br>Состояние: {row['status']}",
        icon=folium.Icon(color=color)
    ).add_to(m)

# Сохранение карты в файл
m.save("73.html")