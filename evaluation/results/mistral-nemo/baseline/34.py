import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузить данные о загрязнении реки Лепси из CSV файла
data = pd.read_csv('lepse_river_pollution.csv')

# Создать GeoDataFrame из данных о загрязнении реки Лепси
geometry = [Point(lon, lat) for lon, lat in zip(data['Longitude'], data['Latitude'])]
gdf = gpd.GeoDataFrame(data, geometry=geometry)

# Создать карту с помощью folium
m = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=12)

# Добавить геообъекты на карту в зависимости от уровня загрязнения воды
for idx, row in gdf.iterrows():
    pollution_level = row['Pollution_Level']
    if pollution_level < 50:
        color = 'green'
    elif pollution_level >= 50 and pollution_level < 100:
        color = 'yellow'
    else:
        color = 'red'

    folium.CircleMarker(location=[row['Latitude'], row['Longitude']],
                        radius=6,
                        color=color,
                        fill=True,
                        fill_color=color).add_to(m)

# Сохранить карту как HTML-файл
m.save("34.html")