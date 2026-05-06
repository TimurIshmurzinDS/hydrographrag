import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# Шаг 1: Сбор данных
river_data = pd.read_csv('river_data.csv')
crop_yield_data = pd.read_csv('crop_yield_data.csv')

# Шаг 2: Подготовка данных
# Добавить геометрию точек к данным о расходе воды в реках
river_data['geometry'] = [Point(xy) for xy in zip(river_data['longitude'], river_data['latitude'])]

# Создать GeoDataFrame для данных о расходе воды в реках
gdf_rivers = gpd.GeoDataFrame(river_data, geometry='geometry')

# Шаг 3: Геопространственный анализ
# Выполнить анализ влияния расхода воды на урожайность сельскохозяйственных культур

# Шаг 4: Визуализация результатов
# Создать карту с использованием библиотеки folium
m = folium.Map(location=[river_data['latitude'].mean(), river_data['longitude'].mean()], zoom_start=8)

# Добавить точки расхода воды в реки на карту
for _, row in gdf_rivers.iterrows():
    folium.CircleMarker(
        location=(row.geometry.y, row.geometry.x),
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)

# Сохранить карту в формате HTML
m.save("110.html")