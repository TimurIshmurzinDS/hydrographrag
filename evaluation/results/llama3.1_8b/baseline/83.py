import pandas as pd
import geopandas as gpd
from folium import Map, Marker

# Шаг 1: Подготовка данных
temirlik_data = pd.read_csv('temirlik_water_usage.csv')
turgen_data = pd.read_csv('turgan_water_usage.csv')

# Шаг 2: Обработка данных
temirlik_data['date'] = pd.to_datetime(temirlik_data['date'])
turgen_data['date'] = pd.to_datetime(turgen_data['date'])

# Удаление пропусков и аномалий
temirlik_data.dropna(inplace=True)
turgen_data.dropna(inplace=True)

# Нормализация значений
temirlik_data['water_usage'] = (temirlik_data['water_usage'] - temirlik_data['water_usage'].min()) / (temirlik_data['water_usage'].max() - temirlik_data['water_usage'].min())
turgen_data['water_usage'] = (turgen_data['water_usage'] - turgen_data['water_usage'].min()) / (turgen_data['water_usage'].max() - turgen_data['water_usage'].min())

# Шаг 3: Создание модели
temirlik_gdf = gpd.GeoDataFrame(temirlik_data, geometry=gpd.points_from_xy(temirlik_data['longitude'], temirlik_data['latitude']))
turgen_gdf = gpd.GeoDataFrame(turgen_data, geometry=gpd.points_from_xy(turgen_data['longitude'], turgen_data['latitude']))

# Группировка данных по месяцам и рекам
temirlik_grouped = temirlik_gdf.groupby([pd.Grouper(key='date', freq='M'), 'name'])['water_usage'].mean().reset_index()
turgen_grouped = turgen_gdf.groupby([pd.Grouper(key='date', freq='M'), 'name'])['water_usage'].mean().reset_index()

# Шаг 4: Анализ и оценка
temirlik_avg_water_usage = temirlik_grouped.groupby('name')['water_usage'].mean()
turgen_avg_water_usage = turgen_grouped.groupby('name')['water_usage'].mean()

# Шаг 5: Визуализация
m = Map(location=[48.0, 69.0], zoom_start=6)
temirlik_marker = Marker(location=[48.0, 69.0], popup='Темирлик').add_to(m)
turgen_marker = Marker(location=[49.0, 70.0], popup='Турген').add_to(m)

# Добавление графика
m.fit_bounds([[45, 65], [50, 75]])

# Сохранение карты как HTML-файл
m.save("83.html")