import folium
from folium.plugins import TimestampedGeoJson

# Загрузим данные о реке Каратал и ее гидрологических станциях.
# Для простоты предположим, что у нас есть база данных с данными о реках и станциях.

import pandas as pd
df_river = pd.DataFrame({
    'name': ['Каратал'],
    'lat': [43.1234],
    'lon': [76.5678]
})

df_station = pd.DataFrame({
    'name': ['Станция Каратал'],
    'lat': [43.1256],
    'lon': [76.5699],
    'sensor_status': ['работает']  # статус датчика уровня воды
})

# Определим местоположение датчика уровня воды.
station_lat = df_station['lat'].values[0]
station_lon = df_station['lon'].values[0]

# Получим текущий статус датчика уровня воды из базы данных или другого источника данных.
# Для простоты предположим, что у нас есть функция get_sensor_status(), которая возвращает статус датчика.

def get_sensor_status(station_name):
    # Имитация получения статуса из базы данных
    return df_station.loc[df_station['name'] == station_name, 'sensor_status'].values[0]

station_status = get_sensor_status('Станция Каратал')

# Визуализируем местоположение реки и гидрологической станции на карте.
m = folium.Map(location=[43.1256, 76.5699], zoom_start=10)

folium.Marker([station_lat, station_lon], popup='Станция Каратал').add_to(m)
folium.Marker([df_river['lat'].values[0], df_river['lon'].values[0]], popup='Река Каратал').add_to(m)

# Добавим информацию о статусе датчика уровня воды.
folium.Marker([station_lat, station_lon],
              popup=f'Станция Каратал: {station_status}').add_to(m)

m.save("2.html")