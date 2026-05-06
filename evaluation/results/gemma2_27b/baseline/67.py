import geopandas as gpd
import folium

# Загрузка данных о постах и уровнях воды (пример)
posts = gpd.read_file("posts_data.geojson") 
water_levels = pd.read_csv("water_levels.csv")

# Объединение данных по ID поста
merged_data = posts.merge(water_levels, on='post_id')

# Создание карты
m = folium.Map(location=[55.75, 37.62], zoom_start=10) # Примерные координаты реки Проходная

# Добавление маркеров на карту
for index, row in merged_data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Пост: {row['post_name']}<br>Уровень воды: {row['water_level']} м",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("67.html")