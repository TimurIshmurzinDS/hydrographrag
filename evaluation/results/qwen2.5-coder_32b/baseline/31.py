import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть два файла CSV:
# - water_flow.csv с данными о водном потоке (дата, координаты, объем воды)
# - water_usage.csv с данными о точках использования воды (название точки, координаты, объем потребляемой воды)

water_flow = pd.read_csv('water_flow.csv')
water_usage = pd.read_csv('water_usage.csv')

# Шаг 2: Обработка данных
# Преобразуем данные в формат GeoDataFrame для работы с геоданными

geometry_flow = [Point(xy) for xy in zip(water_flow['longitude'], water_flow['latitude'])]
gdf_water_flow = gpd.GeoDataFrame(water_flow, geometry=geometry_flow)

geometry_usage = [Point(xy) for xy in zip(water_usage['longitude'], water_usage['latitude'])]
gdf_water_usage = gpd.GeoDataFrame(water_usage, geometry=geometry_usage)

# Удаляем пропуски
gdf_water_flow.dropna(inplace=True)
gdf_water_usage.dropna(inplace=True)

# Шаг 3: Моделирование
# Предположим, что текущий уровень потребления воды можно определить как суммарный объем потребляемой воды за последний месяц

current_month = gdf_water_usage['date'].max().split('-')[0] + '-' + gdf_water_usage['date'].max().split('-')[1]
monthly_usage = gdf_water_usage[gdf_water_usage['date'].str.startswith(current_month)]['volume'].sum()

# Шаг 4: Визуализация
# Создаем карту с использованием folium

m = folium.Map(location=[gdf_water_flow['latitude'].mean(), gdf_water_flow['longitude'].mean()], zoom_start=10)

# Добавляем точки водного потока на карту
for _, row in gdf_water_flow.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        popup=f"Водный поток: {row['volume']} м³/с"
    ).add_to(m)

# Добавляем точки использования воды на карту
for _, row in gdf_water_usage.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=5,
        color='red',
        fill=True,
        fill_color='red',
        popup=f"Потребление: {row['volume']} м³/с"
    ).add_to(m)

# Добавляем легенду
folium.map.LayerControl().add_to(m)
folium.Marker([gdf_water_flow['latitude'].mean(), gdf_water_flow['longitude'].mean()], 
              popup=f"Текущий уровень потребления воды: {monthly_usage} м³/мес").add_to(m)

# Сохраняем карту
m.save("31.html")