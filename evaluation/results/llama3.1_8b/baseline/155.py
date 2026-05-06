import pandas as pd
from folium import Map, Marker, CircleMarker
import geopandas as gpd
import matplotlib.pyplot as plt

# Сбор данных о уровнях воды в реках за различные годы
data = {
    'Year': [2020, 2021, 2022],
    'Bayankol River': [10.5, 11.2, 9.8],
    'Lepsy River': [12.1, 13.5, 11.9]
}
df = pd.DataFrame(data)

# Создание географической модели реки
bayankol_gdf = gpd.read_file('path_to_bayankol_shp')
lepsy_gdf = gpd.read_file('path_to_lepsy_shp')

# Анализ динамики уровней воды в реке
bayankol_avg_level = df['Bayankol River'].mean()
lepsy_avg_level = df['Lepsy River'].mean()

print(f'Средний уровень воды в реке Bayankol: {bayankol_avg_level}')
print(f'Средний уровень воды в реке Lepsy: {lepsy_avg_level}')

# Визуализация результатов анализа на карте
m = Map(location=[50.0, 85.0], zoom_start=8)
Marker([bayankol_gdf.centroid.y, bayankol_gdf.centroid.x], popup='Река Bayankol').add_to(m)
CircleMarker([lepsy_gdf.centroid.y, lepsy_gdf.centroid.x], radius=bayankol_avg_level * 1000).add_to(m)

m.save("155.html")