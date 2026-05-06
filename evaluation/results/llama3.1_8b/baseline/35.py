import pandas as pd
from folium import Map, Marker, CircleMarker
import geopandas as gpd

# Сбор данных (предположим, что данные хранятся в файле 'water_data.csv')
data = pd.read_csv('water_data.csv')

# Обработка данных
data['irrigation_water_usage'] = data['total_water_volume'] * 0.5  # примерная оценка расхода воды на ирригацию

# Геоспатальное моделирование (предположим, что мы используем геоданные для области Аягоз)
geodf = gpd.read_file('ayagoz.shp')

# Создание модели дефицита воды
def calculate_water_deficit(row):
    return row['irrigation_water_usage'] - row['water_volume']

geodf['water_deficit'] = geodf.apply(calculate_water_deficit, axis=1)

# Визуализация результатов на карте
m = Map(location=[46.5, 58.0], zoom_start=8)
for index, row in geodf.iterrows():
    if row['water_deficit'] > 0:
        Marker([row['lat'], row['lon']], popup=f'Дефицит воды: {row["water_deficit"]} м³').add_to(m)

# Сохранение карты
m.save("35.html")