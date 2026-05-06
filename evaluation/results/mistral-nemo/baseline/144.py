import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# 1. Загрузить данные о местоположении датчиков уровня воды и их статусе (наличие или отсутствие оповещений).
data = {
    'id': [1, 2, 3, 4, 5],
    'latitude': [43.25, 42.89, 43.76, 42.01, 43.56],
    'longitude': [76.90, 77.12, 76.54, 77.89, 76.80],
    'alert_status': ['yes', 'no', 'yes', 'no', 'yes']
}

df = pd.DataFrame(data)
geometry = [Point(lon, lat) for lon, lat in zip(df['longitude'], df['latitude'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# 2. Создать геопространственный слой для этих данных
gdf.crs = "EPSG:4326"
gdf.set_index('id', inplace=True)

# 3. Отфильтровать данные, чтобы найти только те датчики, которые находятся в бассейне реки Или.
ili_basin = gpd.read_file("path/to/ili_basin.shp") # Замените на путь к файлу с границами бассейна реки Или
filtered_gdf = gpd.sjoin(gdf, ili_basin, how='inner', predicate='intersects')

# 4. Визуализировать отфильтрованные данные на карте с использованием библиотек `folium` и `geopandas`.
m = folium.Map(location=[filtered_gdf['latitude'].mean(), filtered_gdf['longitude'].mean()], zoom_start=8)

for index, row in filtered_gdf.iterrows():
    if row['alert_status'] == 'yes':
        color = 'red'
    else:
        color = 'green'

    folium.CircleMarker(location=[row['latitude'], row['longitude']],
                        radius=5,
                        color=color).add_to(m)

# 5. Сохранить финальную карту как "144.html".
m.save("144.html")