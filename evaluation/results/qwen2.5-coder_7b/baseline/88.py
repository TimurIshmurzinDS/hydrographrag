import geopandas as gpd
import pandas as pd
import folium

# Загрузка данных о постах на реке Koktal River
posts_data = pd.read_csv('koktal_posts.csv')

# Предположим, что данные о уровне воды содержатся в файле 'water_levels.csv'
water_levels_data = pd.read_csv('water_levels.csv')

# Объединение данных по общему столбцу (например, ID поста)
merged_data = pd.merge(posts_data, water_levels_data, on='post_id')

# Загрузка геоданных о реке Koktal River
river_gdf = gpd.read_file('koktal_river.shp')

# Создание карты
m = folium.Map(location=[river_gdf.geometry.centroid.y.mean(), river_gdf.geometry.centroid.x.mean()], zoom_start=12)

# Добавление геоданных о реке на карту
folium.GeoJson(river_gdf).add_to(m)

# Добавление маркеров постов и уровней воды
for index, row in merged_data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Post ID: {row['post_id']}<br>Water Level: {row['water_level']}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("88.html")