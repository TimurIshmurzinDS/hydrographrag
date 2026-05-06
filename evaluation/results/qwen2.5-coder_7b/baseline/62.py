import pandas as pd
import geopandas as gpd
import folium

# Загрузка данных о постах мониторинга (пример)
data = {
    'post_id': [1, 2, 3, 4, 5],
    'latitude': [50.1, 50.2, 50.3, 50.4, 50.5],
    'longitude': [30.1, 30.2, 30.3, 30.4, 30.5],
    'is_transmitting_data': [True, False, True, False, True]
}

df = pd.DataFrame(data)

# Создание GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

# Фильтрация постов, которые не передают данные
non_transmitting_posts = gdf[gdf['is_transmitting_data'] == False]

# Создание карты
m = folium.Map(location=[50.3, 30.3], zoom_start=12)

# Добавление маркеров для отфильтрованных постов
for idx, row in non_transmitting_posts.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Post ID: {row['post_id']}", icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("62.html")