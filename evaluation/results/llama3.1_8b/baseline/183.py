import pandas as pd
from folium import Map, Marker, CircleMarker
import geopandas as gpd
from shapely.geometry import Point

# Сбор данных (предположим, что данные хранятся в таблице базы данных)
data = {
    'сад': ['Сад 1', 'Сад 2', 'Сад 3'],
    'местоположение_геометрия': [
        Point(55.7558, 37.6173),
        Point(55.7559, 37.6183),
        Point(55.7560, 37.6193)
    ],
    'сток_реки': [10, 20, 30]  # Предположим, что сток реки измеряется в единицах
}

# Обработка данных
df = pd.DataFrame(data)

# Моделирование (предположим, что мы используем простую линейную регрессию)
import numpy as np

def доступность_воды(сток_реки):
    return сток_реки * 0.1 + 5  # Предположим, что доступность воды пропорциональна стоку реки

df['доступность_воды'] = df['сток_реки'].apply(dоступность_воды)

# Визуализация
m = Map(location=[55.7558, 37.6173], zoom_start=12)
for index, row in df.iterrows():
    marker = Marker(
        location=row['местоположение_геометрия'],
        popup=f'Сад: {row["сад"]}<br>Доступность воды: {row["доступность_воды"]}%',
        icon=CircleMarker(radius=5)
    )
    m.add_child(marker)

m.save("183.html")