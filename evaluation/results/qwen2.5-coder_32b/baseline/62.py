import pandas as pd
import folium

# Предположим, что у нас есть DataFrame с данными о мониторинговых постах
# В реальности данные могут быть загружены из файла или базы данных
data = {
    'post_id': [1, 2, 3, 4, 5],
    'latitude': [50.789, 50.800, 50.811, 50.822, 50.833],
    'longitude': [76.543, 76.554, 76.565, 76.576, 76.587],
    'status': ['active', 'inactive', 'active', 'inactive', 'active']  # 'active' - передает данные, 'inactive' - не передает
}

# Создаем DataFrame из словаря
df = pd.DataFrame(data)

# Фильтруем посты, которые не передают данные
non_transmitting_posts = df[df['status'] == 'inactive']

# Создаем карту с центром в средних координатах всех постов
map_center = [df['latitude'].mean(), df['longitude'].mean()]
m = folium.Map(location=map_center, zoom_start=10)

# Добавляем маркеры на карту для каждого мониторингового поста
for _, row in df.iterrows():
    if row['status'] == 'active':
        icon_color = 'green'
    else:
        icon_color = 'red'
    
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Пост ID: {row['post_id']}<br>Статус: {row['status']}",
        icon=folium.Icon(color=icon_color)
    ).add_to(m)

# Сохраняем карту в файл
m.save("62.html")