import pandas as pd
import folium

# Загрузка данных о высотах уровня воды и координатах гидрологических постов
data = {
    'post_name': ['Post1', 'Post2', 'Post3', 'Post4'],
    'latitude': [50.1, 50.2, 50.3, 50.4],
    'longitude': [60.1, 60.2, 60.3, 60.4],
    'water_level': [100, 105, 98, 110]
}

df = pd.DataFrame(data)

# Определение критического уровня
critical_level = 100

# Фильтрация данных
critical_posts = df[df['water_level'] > critical_level]

# Создание карты
m = folium.Map(location=[50.2, 60.2], zoom_start=13)

# Добавление маркеров критических постов
for index, row in critical_posts.iterrows():
    folium.Marker([row['latitude'], row['longitude']], 
                  popup=f"Post: {row['post_name']}, Water Level: {row['water_level']}").add_to(m)

# Сохранение карты
m.save("70.html")