import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import folium
from scipy.interpolate import griddata
import numpy as np

# Шаг 1: Сбор данных
# Предположим, что у нас есть CSV файл с данными о водном уровне реки Шарын и GeoJSON файл с картографическими данными экосистем.
water_level_data = pd.read_csv('sharyn_water_level.csv')  # Пример файла с данными о водном уровне
ecosystems_gdf = gpd.read_file('ecosystems.geojson')     # Пример файла с картографическими данными экосистем

# Шаг 2: Подготовка данных
# Преобразуем данные о водном уровне в формат, удобный для моделирования.
water_level_data['date'] = pd.to_datetime(water_level_data['date'])
latest_water_levels = water_level_data.groupby('station').last().reset_index()

# Шаг 3: Анализ изменений уровня воды
# Предположим, что мы уже проанализировали данные и выбрали наиболее актуальные значения для моделирования.

# Шаг 4: Моделирование влияния на экосистемы
# Используем метод интерполяции для создания сетки значений уровня воды.
grid_x, grid_y = np.mgrid[ecosystems_gdf.total_bounds[0]:ecosystems_gdf.total_bounds[2]:100j,
                         ecosystems_gdf.total_bounds[1]:ecosystems_gdf.total_bounds[3]:100j]
points = latest_water_levels[['longitude', 'latitude']].values
values = latest_water_levels['water_level'].values

grid_z = griddata(points, values, (grid_x, grid_y), method='cubic')

# Шаг 5: Оценка биоразнообразия
# Предположим, что у нас есть данные о биоразнообразии в виде столбца 'biodiversity_index' в GeoDataFrame.
ecosystems_gdf['water_level'] = ecosystems_gdf.apply(lambda row: griddata(points, values, (row.geometry.centroid.x, row.geometry.centroid.y), method='cubic'), axis=1)
ecosystems_gdf['impact_on_biodiversity'] = ecosystems_gdf['biodiversity_index'] * ecosystems_gdf['water_level']

# Шаг 6: Визуализация результатов
m = folium.Map(location=[ecosystems_gdf.total_bounds[1] + (ecosystems_gdf.total_bounds[3] - ecosystems_gdf.total_bounds[1]) / 2,
                         ecosystems_gdf.total_bounds[0] + (ecosystems_gdf.total_bounds[2] - ecosystems_gdf.total_bounds[0]) / 2],
               zoom_start=10)

# Добавление данных о водном уровне на карту
folium.Choropleth(
    geo_data=ecosystems_gdf,
    name='choropleth',
    data=ecosystems_gdf,
    columns=['id', 'impact_on_biodiversity'],
    key_on='feature.properties.id',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Влияние уровня воды на биоразнообразие'
).add_to(m)

folium.LayerControl().add_to(m)
m.save("181.html")