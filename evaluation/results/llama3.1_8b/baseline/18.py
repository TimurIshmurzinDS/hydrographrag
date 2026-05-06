import pandas as pd
from folium import Map, Marker, CircleMarker, Polygon, FeatureGroup, GeoJson
from folium.plugins import HeatMap
import geopandas as gpd
import matplotlib.pyplot as plt

# Шаг 1: Сбор данных о реке и ее гидрологических характеристиках.
river_data = pd.DataFrame({
    'name': ['Bayankol River'],
    'latitude': [48.1234],
    'longitude': [87.4567]
})

# Шаг 2: Анализ исторических данных о паводках на реке.
pavodki_data = pd.DataFrame({
    'date': ['2020-01-01', '2020-06-15'],
    'water_level': [10, 20],
    'location': ['Point A', 'Point B']
})

# Шаг 3: Создание модели прогнозирования паводков на основе анализа исторических данных.
def predict_pavodki(water_level):
    if water_level > 15:
        return True
    else:
        return False

# Шаг 4: Получение предупреждений о сезонных паводках на основе прогноза.
warnings = []
for index, row in pavodki_data.iterrows():
    if predict_pavodki(row['water_level']):
        warnings.append({
            'date': row['date'],
            'location': row['location']
        })

# Шаг 5: Визуализация предупреждений на карте.
m = Map(location=[48.1234, 87.4567], zoom_start=10)
feature_group = FeatureGroup(name='Предупреждения о паводках')

for warning in warnings:
    marker = Marker(
        location=[warning['location'].split(' ')[0], warning['location'].split(' ')[1]],
        popup=f'Предупреждение о паводке на {warning["date"]}',
        icon=CircleMarker(radius=5, color='red')
    )
    feature_group.add_child(marker)

m.add_child(feature_group)
m.save("18.html")