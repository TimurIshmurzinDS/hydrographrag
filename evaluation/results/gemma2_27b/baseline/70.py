import folium
import pandas as pd

# Загрузка данных о гидрологических постах (замените на актуальные данные)
posts = pd.read_csv("hydrological_posts.csv") 

# Загрузка данных об уровнях воды (замените на актуальные данные)
water_levels = pd.read_csv("water_levels.csv")

# Определение критического уровня (замените на актуальный уровень)
critical_level = 5.0

# Сопоставление данных о постах и уровнях воды
merged_data = pd.merge(posts, water_levels, on='post_id')

# Выделение постов с критическим уровнем
critical_posts = merged_data[merged_data['water_level'] >= critical_level]

# Создание карты
m = folium.Map(location=[critical_posts['latitude'].mean(), critical_posts['longitude'].mean()], zoom_start=10)

# Добавление маркеров для постов с критическим уровнем
for index, row in critical_posts.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Пост {row['post_id']}: Уровень воды {row['water_level']} м",
        icon=folium.Icon(color='red', icon='warning-sign')
    ).add_to(m)

# Сохранение карты
m.save("70.html")