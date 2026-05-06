import pandas as pd
from folium import Map, Marker, CircleMarker
import geopandas as gpd

# Сбор данных о реках и их характеристиках
data = {
    'River': ['Kurty River', 'Urzhar River', 'Byzhy River'],
    'Length (km)': [120, 150, 100],
    'Width (m)': [10, 15, 12],
    'Speed (m/s)': [0.5, 1.2, 0.8]
}

df = pd.DataFrame(data)

# Создание модели водопотребления
def calculate_water_consumption(length, width, speed):
    return length * width * speed

# Вычисление уровней водопотребления для каждой реки
water_consumptions = df.apply(lambda row: calculate_water_consumption(row['Length (km)'], row['Width (m)'], row['Speed (m/s)']), axis=1)

# Визуализация результатов на карте
m = Map(location=[50.0, 70.0], zoom_start=6)
for i, river in enumerate(df['River']):
    water_consumption = water_consumptions[i]
    marker = Marker([df.loc[i, 'Length (km)'] / 100000, df.loc[i, 'Width (m)']], popup=f'Водопотребление в {river}: {water_consumption} м³/с')
    m.add_child(marker)

# Сохранение карты
m.save("112.html")