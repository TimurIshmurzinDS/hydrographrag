import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузка данных о расходе воды в реках Или и Шизжин
data_ili = pd.read_csv('ili_water_data.csv')
data_shyzhyn = pd.read_csv('shyzhyn_water_data.csv')

# Создание географических объектов для каждой реки
gdf_ili = gpd.GeoDataFrame(data_ili, geometry=gpd.points_from_xy(data_ili.longitude, data_ili.latitude))
gdf_shyzhyn = gpd.GeoDataFrame(data_shyzhyn, geometry=gpd.points_from_xy(data_shyzhyn.longitude, data_shyzhyn.latitude))

# Анализ данных о расходе воды в зависимости от времени года (сезона)
seasonal_water_usage_ili = gdf_ili.groupby('season')['water_usage'].mean()
seasonal_water_usage_shyzhyn = gdf_shyzhyn.groupby('season')['water_usage'].mean()

# Сравнение результатов анализа для обеих рек
comparison_results = pd.DataFrame({'Или': seasonal_water_usage_ili, 'Шизжин': seasonal_water_usage_shyzhyn})

# Визуализация результатов на карте с помощью библиотеки Folium
m = folium.Map(location=[46.5, 68], zoom_start=8)
folium.Choropleth(
    geo_data=gdf_ili.geometry,
    data=comparison_results,
    columns=['Или', 'Шизжин'],
    key_on='feature.properties.name',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)
m.save("160.html")