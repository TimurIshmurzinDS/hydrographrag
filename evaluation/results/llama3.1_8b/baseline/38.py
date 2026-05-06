import pandas as pd
from folium import Map, Marker, CircleMarker
import geopandas as gpd
from shapely.geometry import Point

# Шаг 1: Сбор данных
data = {
    'name': ['Каркара'],
    'geometry': [Point(55.1234, 37.5678)],
    'source_pollution': [10],
    'water_speed': [2],
    'river_depth': [5]
}
df = pd.DataFrame(data)

# Шаг 2: Создание модели
def calculate_risk(row):
    risk = row['source_pollution'] * row['water_speed'] / row['river_depth']
    return risk

df['risk'] = df.apply(calculate_risk, axis=1)

# Шаг 3: Оценка экологического риска
max_risk = df['risk'].max()
min_risk = df['risk'].min()

# Шаг 4: Визуализация результатов
m = Map(location=[55.1234, 37.5678], zoom_start=10)
marker = Marker(location=df['geometry'][0], popup='Река Каркара', icon=None).add_to(m)

circle = CircleMarker(
    location=df['geometry'][0],
    radius=max_risk * 100,
    color='red',
    fill=True,
    fill_color='red'
).add_to(m)

m.save("38.html")