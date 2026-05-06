import folium

# Пример данных о гидрометрических постах на реке Koktal River
data = [
    {"name": "Пост 1", "coordinates": [42.50, 76.90], "water_level": 123.4},
    {"name": "Пост 2", "coordinates": [42.55, 76.85], "water_level": 130.2},
    {"name": "Пост 3", "coordinates": [42.45, 76.95], "water_level": 118.7},
]

# Создание карты с центром в средней точке всех постов
map_center = [
    sum(point["coordinates"][0] for point in data) / len(data),
    sum(point["coordinates"][1] for point in data) / len(data)
]
m = folium.Map(location=map_center, zoom_start=12)

# Добавление маркеров на карту для каждого поста
for post in data:
    folium.Marker(
        location=post["coordinates"],
        popup=f"Пост: {post['name']}\nУровень воды: {post['water_level']} м",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("88.html")

# Вывод списка постов и их уровней воды
for post in data:
    print(f"Пост: {post['name']}, Уровень воды: {post['water_level']} м")