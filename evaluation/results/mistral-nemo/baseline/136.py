import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# 1. Загрузить данные о датчиках уровня воды и их местоположении из базы данных или файла.
data = pd.read_csv('water_level_sensors.csv')

# 2. Создать географическую проекцию для работы с данными.
geometry = [Point(xy) for xy in zip(data['longitude'], data['latitude'])]
gdf = gpd.GeoDataFrame(data, geometry=geometry)
gdf.crs = 'EPSG:4326'  # Установить CRS для геоданных

# 3. Проанализировать статус каждого датчика уровня воды в речной сети региона.
status_counts = gdf['status'].value_counts()

# 4. Визуализировать результаты на карте, используя библиотеку `folium`.
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

for _, row in gdf.iterrows():
    folium.CircleMarker(
        location=(row.geometry.y, row.geometry.x),
        radius=5,
        color='blue' if row['status'] == 'active' else 'gray',
        fill=True
    ).add_to(m)

# 5. Сохранить финальную карту как "136.html".
m.save("136.html")