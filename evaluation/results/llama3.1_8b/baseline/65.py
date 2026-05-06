import pandas as pd
from folium import Map, Marker, Icon
import numpy as np

# Загрузим данные о уровнях воды с датчиков (предположим, что они хранятся в файлах csv)
data_akasu = pd.read_csv('akasu_water_levels.csv')
data_byzhy = pd.read_csv('byzhy_water_levels.csv')

# Проверим, неисправны ли датчики
def check_sensors(data):
    # Если нет данных за последние 24 часа, датчик считается неисправным
    if data['timestamp'].max() - data['timestamp'].min() > pd.Timedelta(days=1):
        return True
    else:
        return False

# Проверим датчики на обоих реках
akasu_sensors_ok = not check_sensors(data_akasu)
byzhy_sensors_ok = not check_sensors(data_byzhy)

# Если датчики неисправны, сообщим об этом в отчете
if not akasu_sensors_ok:
    print("Датчик на реке Аксу неисправен!")
if not byzhy_sensors_ok:
    print("Датчик на реке Быжь неисправен!")

# Визуализируем данные о уровнях воды на карте
m = Map(location=[45.0, 55.0], zoom_start=6)

# Добавим маркеры для обоих рек
Marker([data_akasu['latitude'].mean(), data_akusu['longitude'].mean()], 
       icon=Icon(color='blue'), popup='Река Аксу').add_to(m)
Marker([data_byzhy['latitude'].mean(), data_byzhy['longitude'].mean()], 
       icon=Icon(color='red'), popup='Река Быжь').add_to(m)

# Добавим слой для отображения данных о уровнях воды
for i, row in data_akasu.iterrows():
    Marker([row['latitude'], row['longitude']], 
           icon=Icon(color='blue' if row['water_level'] < 10 else 'red'), 
           popup=f"Уровень воды: {row['water_level']}").add_to(m)
for i, row in data_byzhy.iterrows():
    Marker([row['latitude'], row['longitude']], 
           icon=Icon(color='blue' if row['water_level'] < 10 else 'red'), 
           popup=f"Уровень воды: {row['water_level']}").add_to(m)

# Сохраняем карту в файл
m.save("65.html")