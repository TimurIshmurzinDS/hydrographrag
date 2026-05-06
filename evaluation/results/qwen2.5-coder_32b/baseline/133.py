import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Предположим, что у нас есть данные о водном уровне рек в формате CSV
# Структура данных: date, river_name, water_level, latitude, longitude

# Загрузка данных
dos_data = pd.read_csv('dos_river_data.csv')
kurty_data = pd.read_csv('kurty_river_data.csv')

# Преобразование данных в формат временных рядов
dos_data['date'] = pd.to_datetime(dos_data['date'])
kurty_data['date'] = pd.to_datetime(kurty_data['date'])

# Определение актуального и исторического периодов
current_period_start = '2023-10-01'
current_period_end = '2023-10-31'
historical_period_start = '2022-10-01'
historical_period_end = '2022-10-31'

# Фильтрация данных по периодам
dos_current = dos_data[(dos_data['date'] >= current_period_start) & (dos_data['date'] <= current_period_end)]
dos_historical = dos_data[(dos_data['date'] >= historical_period_start) & (dos_data['date'] <= historical_period_end)]

kurty_current = kurty_data[(kurty_data['date'] >= current_period_start) & (kurty_data['date'] <= current_period_end)]
kurty_historical = kurty_data[(kurty_data['date'] >= historical_period_start) & (kurty_data['date'] <= historical_period_end)]

# Вычисление среднего водного уровня за периоды
dos_current_avg = dos_current.groupby('date')['water_level'].mean().reset_index()
dos_historical_avg = dos_historical.groupby('date')['water_level'].mean().reset_index()

kurty_current_avg = kurty_current.groupby('date')['water_level'].mean().reset_index()
kurty_historical_avg = kurty_historical.groupby('date')['water_level'].mean().reset_index()

# Создание геодатафреймов для стоков рек
dos_location = Point(dos_data['longitude'].iloc[0], dos_data['latitude'].iloc[0])
kurty_location = Point(kurty_data['longitude'].iloc[0], kurty_data['latitude'].iloc[0])

gdf_dos = gpd.GeoDataFrame({'river': ['Dos River'], 'geometry': [dos_location]})
gdf_kurty = gpd.GeoDataFrame({'river': ['Kurty River'], 'geometry': [kurty_location]})

# Создание карты с использованием folium
m = folium.Map(location=[(dos_data['latitude'].iloc[0] + kurty_data['latitude'].iloc[0]) / 2,
                         (dos_data['longitude'].iloc[0] + kurty_data['longitude'].iloc[0]) / 2], zoom_start=10)

# Добавление маркеров для стоков рек
folium.Marker(
    location=[gdf_dos.geometry.y.iloc[0], gdf_dos.geometry.x.iloc[0]],
    popup='Dos River',
    icon=folium.Icon(color='blue')
).add_to(m)

folium.Marker(
    location=[gdf_kurty.geometry.y.iloc[0], gdf_kurty.geometry.x.iloc[0]],
    popup='Kurty River',
    icon=folium.Icon(color='red')
).add_to(m)

# Добавление временных рядов водного уровня на карту
for idx, row in dos_current_avg.iterrows():
    folium.CircleMarker(
        location=[gdf_dos.geometry.y.iloc[0], gdf_dos.geometry.x.iloc[0]],
        radius=row['water_level'] / 10,  # Уменьшение радиуса для визуализации
        color='blue',
        fill=True,
        fill_color='blue',
        popup=f'Date: {row["date"].strftime("%Y-%m-%d")}, Water Level: {row["water_level"]}'
    ).add_to(m)

for idx, row in kurty_current_avg.iterrows():
    folium.CircleMarker(
        location=[gdf_kurty.geometry.y.iloc[0], gdf_kurty.geometry.x.iloc[0]],
        radius=row['water_level'] / 10,  # Уменьшение радиуса для визуализации
        color='red',
        fill=True,
        fill_color='red',
        popup=f'Date: {row["date"].strftime("%Y-%m-%d")}, Water Level: {row["water_level"]}'
    ).add_to(m)

# Сохранение карты
m.save("133.html")