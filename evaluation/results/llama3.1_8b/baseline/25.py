import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузите данные о расходе воды в реках Tekes River и Bayankol River во время паводка.
data_tekes = pd.read_csv('tekess.csv')
data_bayankol = pd.read_csv('bayankol.csv')

# Создайте географические модели расхода воды в реках, используя данные о расходе воды и географических координатах точек наблюдения.
gdf_tekes = gpd.GeoDataFrame(data_tekes, geometry=gpd.points_from_xy(data_tekes.Longitude, data_tekes.Latitude))
gdf_bayankol = gpd.GeoDataFrame(data_bayankol, geometry=gpd.points_from_xy(data_bayankol.Longitude, data_bayankol.Latitude))

# Сравните уровни расхода воды в реках Tekes River и Bayankol River во время паводка.
correlation = gdf_tekes['WaterLevel'].corr(gdf_bayankol['WaterLevel'])
print(f'Коэффициент корреляции: {correlation}')

# Создайте карту с уровнями расхода воды в реках Tekes River и Bayankol River во время паводка.
m = folium.Map(location=[42.5, 79], zoom_start=10)
folium.Choropleth(
    geo_data=gdf_tekes.geometry,
    name='Река Текес',
    data=data_tekes,
    columns=['WaterLevel'],
    key_on='feature.properties.id',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)
folium.Choropleth(
    geo_data=gdf_bayankol.geometry,
    name='Река Баянколь',
    data=data_bayankol,
    columns=['WaterLevel'],
    key_on='feature.properties.id',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)
m.save("25.html")