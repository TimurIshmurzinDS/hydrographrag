import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# Загрузка данных о реках в DataFrame GeoPandas
rivers_data = {
    'Улькен Алматы': (43.25, 71.36),
    'Емель': (43.08, 71.19),
    'Тентек': (43.22, 71.44)
}
gdf = gpd.GeoDataFrame(rivers_data, geometry=gpd.points_from_xy([x[0] for x in rivers_data.values()], [y[1] for y in rivers_data.values()]))

# Фильтрация рек по списку и координатам
selected_rivers = ['Улькен Алматы', 'Емель', 'Тентек']
filtered_gdf = gdf[gdf.index.isin(selected_rivers)]

# Визуализация на карте с помощью Folium
m = folium.Map(location=[43.25, 71.36], zoom_start=10)

for idx, row in filtered_gdf.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup=idx).add_to(m)

# Сохранение карты в файл HTML
m.save("105.html")