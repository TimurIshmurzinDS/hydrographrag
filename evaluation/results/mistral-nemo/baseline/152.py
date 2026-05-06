import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# 1. Подготовка данных
lepsy_data = pd.read_csv('lepsy_river.csv')
shilik_data = pd.read_csv('shilik_river.csv')

# 2. Преобразование данных
lepsy_gdf = gpd.GeoDataFrame(lepsy_data, geometry=gpd.points_from_xy(lepsy_data['lon'], lepsy_data['lat']))
shilik_gdf = gpd.GeoDataFrame(shilik_data, geometry=gpd.points_from_xy(shilik_data['lon'], shilik_data['lat']))

# 3. Моделирование стока
# Предполагается, что у вас есть функция для моделирования гидрологического стока, например, hydro_model()
lepsy_seasonal_flow = hydro_model(lepsy_gdf)
shilik_seasonal_flow = hydro_model(shilik_gdf)

# 4. Визуализация результатов
m = folium.Map(location=[50, 60], zoom_start=8) # Задайте начальную точку и масштаб карты

for idx, row in lepsy_gdf.iterrows():
    folium.CircleMarker(
        location=(row['lat'], row['lon']),
        radius=lepsy_seasonal_flow[idx]*2,
        color='blue',
        fill=True
    ).add_to(m)

for idx, row in shilik_gdf.iterrows():
    folium.CircleMarker(
        location=(row['lat'], row['lon']),
        radius=shilik_seasonal_flow[idx]*2,
        color='red',
        fill=True
    ).add_to(m)

# Сохранение карты в файл HTML
m.save("152.html")