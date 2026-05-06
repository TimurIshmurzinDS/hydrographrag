import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Предположим, что у нас есть геоданные о речных экосистемах в формате GeoJSON
sharyn_gdf = gpd.read_file('sharyn_ecosystems.geojson')
urzhar_gdf = gpd.read_file('urzhar_ecosystems.geojson')

# Предположим, что у нас есть данные о параметрах воды для каждого бассейна в формате CSV
sharyn_water_data = pd.read_csv('sharyn_water_data.csv')
urzhar_water_data = pd.read_csv('urzhar_water_data.csv')

# Пример данных (замените на реальные данные)
data_sharyn = {
    'id': [1, 2],
    'temperature': [7.5, 8.0],
    'pH': [7.2, 6.9]
}
sharyn_water_data = pd.DataFrame(data_sharyn)

data_urzhar = {
    'id': [1, 2],
    'temperature': [7.3, 7.8],
    'pH': [7.4, 7.0]
}
urzhar_water_data = pd.DataFrame(data_urzhar)

# Объединение геоданных с данными о параметрах воды
sharyn_gdf = sharyn_gdf.merge(sharyn_water_data, on='id')
urzhar_gdf = urzhar_gdf.merge(urzhar_water_data, on='id')

# Простая функция для оценки экологического статуса (пример)
def evaluate_ecological_status(row):
    if row['temperature'] < 8.0 and row['pH'] > 6.5:
        return 'Хорошо'
    elif row['temperature'] >= 8.0 or row['pH'] <= 6.5:
        return 'Умеренно'
    else:
        return 'Плохо'

sharyn_gdf['status'] = sharyn_gdf.apply(evaluate_ecological_status, axis=1)
urzhar_gdf['status'] = urzhar_gdf.apply(evaluate_ecological_status, axis=1)

# Создание интерактивной карты с использованием folium
m = folium.Map(location=[50.45, 83.62], zoom_start=9)  # Координаты примерного центра бассейнов

# Добавление точек для реки Шарын
for _, row in sharyn_gdf.iterrows():
    folium.CircleMarker(
        location=[row['geometry'].y, row['geometry'].x],
        radius=5,
        color='green' if row['status'] == 'Хорошо' else ('orange' if row['status'] == 'Умеренно' else 'red'),
        fill=True,
        popup=f"ID: {row['id']}<br>Температура: {row['temperature']}°C<br>pH: {row['pH']}<br>Статус: {row['status']}"
    ).add_to(m)

# Добавление точек для реки Уржар
for _, row in urzhar_gdf.iterrows():
    folium.CircleMarker(
        location=[row['geometry'].y, row['geometry'].x],
        radius=5,
        color='blue' if row['status'] == 'Хорошо' else ('yellow' if row['status'] == 'Умеренно' else 'purple'),
        fill=True,
        popup=f"ID: {row['id']}<br>Температура: {row['temperature']}°C<br>pH: {row['pH']}<br>Статус: {row['status']}"
    ).add_to(m)

# Сохранение карты в HTML файл
m.save("188.html")