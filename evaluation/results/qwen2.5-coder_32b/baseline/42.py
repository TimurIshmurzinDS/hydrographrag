import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium
from scipy.interpolate import griddata
import numpy as np

# Шаг 1: Сбор данных
# Предположим, у нас есть два файла: один с данными о качестве воды и другой с данными об агрокультурных землях.
water_quality_data = pd.read_csv('water_quality.csv')  # Пример: 'station_id', 'nitrate_concentration'
agricultural_land_data = gpd.read_file('agricultural_land.shp')  # Пример: полигонные данные о полях

# Шаг 2: Подготовка данных
# Преобразуем данные о качестве воды в геодатафрейм
geometry = [Point(xy) for xy in zip(water_quality_data['longitude'], water_quality_data['latitude'])]
water_gdf = gpd.GeoDataFrame(water_quality_data, geometry=geometry)

# Шаг 3: Пространственное моделирование
# Интерполяция данных о концентрации нитратов для создания карты
grid_x, grid_y = np.mgrid[min(water_gdf.geometry.x):max(water_gdf.geometry.x):100j,
                         min(water_gdf.geometry.y):max(water_gdf.geometry.y):100j]
points = np.array([(p.x, p.y) for p in water_gdf.geometry])
values = water_gdf['nitrate_concentration']
grid_z = griddata(points, values, (grid_x, grid_y), method='cubic')

# Шаг 4: Анализ влияния агрокультуры
# Простой пример корреляции между интенсивностью использования земель под агрокультуру и концентрацией нитратов
agricultural_intensity = agricultural_land_data['intensity']  # Предположим, что есть поле 'intensity'
correlation = water_gdf['nitrate_concentration'].corr(agricultural_intensity)

# Шаг 5: Визуализация результатов
# Создание интерактивной карты с помощью folium
m = folium.Map(location=[water_gdf.geometry.y.mean(), water_gdf.geometry.x.mean()], zoom_start=10)

# Добавление точек качества воды на карту
for _, row in water_gdf.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=row['nitrate_concentration'] * 2,  # Размер круга пропорционален концентрации нитратов
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)

# Добавление полигонов агрокультурных земель на карту
agricultural_land_data.explore(
    m=m,
    column="intensity",
    cmap="YlGnBu",
    tooltip=["intensity"],
    legend=True
)

# Сохранение карты в файл
m.save("42.html")