import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# Предположим, что у нас есть гидрографическая карта и данные о реках в формате GeoJSON
rivers_gdf = gpd.read_file('path_to_rivers.geojson')
sarykan_basin_gdf = gpd.read_file('path_to_sarykan_basin.geojson')

# Фильтрация рек, которые находятся внутри бассейна Сарыкана Реки
rivers_in_basin = rivers_gdf[rivers_gdf.intersects(sarykan_basin_gdf.unary_union)]

# Предположим, что у нас есть временные ряды уровней воды для каждой реки в формате CSV
# Файл содержит столбцы: 'river_id', 'date', 'water_level'
water_levels_df = pd.read_csv('path_to_water_levels.csv')

# Преобразование даты к datetime формату
water_levels_df['date'] = pd.to_datetime(water_levels_df['date'])

# Определение весенних половодий (например, период с марта по май)
spring_floods_df = water_levels_df[(water_levels_df['date'].dt.month >= 3) & (water_levels_df['date'].dt.month <= 5)]

# Группировка данных по рекам и вычисление среднего уровня воды за весенний период
mean_water_levels_spring = spring_floods_df.groupby('river_id')['water_level'].mean().reset_index()

# Определение порогового значения для классификации риска половодий (например, уровень выше среднего на 10%)
threshold_factor = 1.1
mean_water_levels_all = water_levels_df.groupby('river_id')['water_level'].mean().reset_index()
mean_water_levels_all['spring_risk'] = mean_water_levels_spring.set_index('river_id')['water_level'] / mean_water_levels_all.set_index('river_id')['water_level']
rivers_at_risk = mean_water_levels_all[mean_water_levels_all['spring_risk'] >= threshold_factor]

# Объединение данных о риске с геоданными рек
rivers_in_basin['river_id'] = rivers_in_basin.index  # Предположим, что индекс является идентификатором реки
rivers_at_risk_gdf = gpd.sjoin(rivers_in_basin.set_index('river_id'), rivers_at_risk.set_index('river_id'), how='inner', op='index')

# Визуализация результатов на карте с использованием folium
m = folium.Map(location=[rivers_at_risk_gdf.centroid.y.mean(), rivers_at_risk_gdf.centroid.x.mean()], zoom_start=10)

folium.GeoJson(sarykan_basin_gdf, name='Бассейн Сарыкана Реки').add_to(m)
folium.GeoJson(rivers_in_basin, name='Реки в бассейне', style_function=lambda x: {'color': 'blue'}).add_to(m)
folium.GeoJson(rivers_at_risk_gdf, name='Реки с высоким риском половодий', style_function=lambda x: {'color': 'red'}).add_to(m)

folium.LayerControl().add_to(m)
m.save("153.html")