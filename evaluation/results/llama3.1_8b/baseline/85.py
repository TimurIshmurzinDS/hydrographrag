import pandas as pd
from folium import Map, Marker, CircleMarker
import geopandas as gpd
import matplotlib.pyplot as plt

# Подготовка данных
koktal_data = pd.DataFrame({
    'river': ['Koktal River'],
    'flow_rate': [10.5],
    'water_level': [2.8]
})

baskan_data = pd.DataFrame({
    'river': ['Baskan River'],
    'flow_rate': [7.2],
    'water_level': [1.9]
})

# Объединение данных
data = pd.concat([koktal_data, baskan_data])

# Создание геопанды с данными
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['flow_rate'], data['water_level']))

# Моделирование затопления
def calculate_risk(flow_rate, water_level):
    # Простая модель для демонстрации: риск пропорционален расходу воды и высоте реки
    return flow_rate * water_level

gdf['risk'] = gdf.apply(lambda row: calculate_risk(row['flow_rate'], row['water_level']), axis=1)

# Анализ риска
high_risk_areas = gdf[gdf['risk'] > 20]

# Визуализация на карте
m = Map(location=[45.0, 75.0], zoom_start=10)
for index, row in high_risk_areas.iterrows():
    Marker(row.geometry.y, row.geometry.x).add_to(m)

m.save("85.html")