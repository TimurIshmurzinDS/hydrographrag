import pandas as pd
from folium import Map, Marker, CircleMarker
import geopandas as gpd
from shapely.geometry import Point

# Загрузим данные о характеристиках рек
data_byzhy = {
    'name': ['Byzhy River'],
    'length': [100],
    'width': [10],
    'speed': [1]
}
df_byzhy = pd.DataFrame(data_byzhy)

data_tekeli = {
    'name': ['Tekeli River'],
    'length': [120],
    'width': [12],
    'speed': [1.2]
}
df_tekeli = pd.DataFrame(data_tekeli)

# Создадим экологические индикаторы
def calculate_water_quality(df):
    df['water_quality'] = (df['length'] + df['width']) / 2 * df['speed']
    return df

df_byzhy = calculate_water_quality(df_byzhy)
df_tekeli = calculate_water_quality(df_tekeli)

# Сравним экологические индикаторы
def compare_indicators(df1, df2):
    df_compare = pd.merge(df1, df2, on='name', suffixes=('_byzhy', '_tekeli'))
    return df_compare

df_compare = compare_indicators(df_byzhy, df_tekeli)

# Визуализируем результаты на карте
m = Map(location=[50.0, 70.0], zoom_start=6)
for index, row in df_compare.iterrows():
    lat = 50.0 + (row['length'] / 100) * 10
    lon = 70.0 + (row['width'] / 10) * 5
    Marker(location=[lat, lon], popup=f"Индикатор чистоты воды: {row['water_quality_byzhy']}").add_to(m)
    CircleMarker(location=[lat, lon], radius=row['speed'], color='red').add_to(m)

m.save("119.html")