import geopandas as gpd
import pandas as pd
import folium

# Шаг 1: Подготовка данных
rivers_gdf = gpd.read_file('rivers.shp')
water_levels_df = pd.read_csv('water_levels.csv')

# Шаг 2: Обработка данных
# Создаем таблицу для хранения данных о реках и уровнях воды
rivers_water_levels_gdf = rivers_gdf.merge(water_levels_df, on='river_id', how='left')

# Определяем реки, на которых уровень воды превышает норму
exceeding_rivers_gdf = rivers_water_levels_gdf[rivers_water_levels_gdf['water_level'] > rivers_water_levels_gdf['normal_level']]

# Шаг 3: Визуализация результатов
m = folium.Map(location=[55.7558, 37.6173], zoom_start=10)

for index, row in exceeding_rivers_gdf.iterrows():
    folium.Marker([row['y'], row['x']], popup=row['river_name']).add_to(m)

# Сохраняем карту в файл
m.save("81.html")