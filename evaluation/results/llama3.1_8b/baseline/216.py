import pandas as pd
from folium import Map, Marker

# Загрузка данных о реке Karaoy River и ее сенсорах
river_data = pd.read_csv('karaoy_river.csv')
sensor_data = pd.read_csv('sensors.csv')

# Создание функции телепортации
def teleport_object(object_id):
    # Получение координат объекта из базы данных
    object_coords = river_data.loc[river_data['object_id'] == object_id, ['x', 'y']].values
    
    # Получение сенсоров вдоль реки
    sensors_along_river = sensor_data[sensor_data['river_id'] == 1]
    
    # Определение типов сенсоров и их расположения
    gps_sensors = sensors_along_river[sensors_along_river['sensor_type'] == 'GPS']
    accelerometer_sensors = sensors_along_river[sensors_along_river['sensor_type'] == 'акселерометр']
    
    # Телепортация объекта по сенсорам
    new_coords = []
    for i in range(len(gps_sensors)):
        gps_coord = gps_sensors.iloc[i]['x'], gps_sensors.iloc[i]['y']
        accelerometer_coord = accelerometer_sensors.iloc[i]['x'], accelerometer_sensors.iloc[i]['y']
        new_coords.append((gps_coord[0] + accelerometer_coord[0], gps_coord[1] + accelerometer_coord[1]))
    
    # Возвращение новых координат объекта
    return new_coords

# Создание функции визуализации на карте
def visualize_on_map(object_id):
    m = Map(location=[55.7558, 37.6173], zoom_start=10)
    new_coords = teleport_object(object_id)
    
    for i in range(len(new_coords)):
        Marker(location=new_coords[i]).add_to(m)
    
    # Сохранение карты в файл
    m.save("216.html")

# Использование функций телепортации и визуализации
object_id = 1
new_coords = teleport_object(object_id)
visualize_on_map(object_id)