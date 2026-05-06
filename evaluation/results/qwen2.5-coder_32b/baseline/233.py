import folium

# Координаты примерного центра павода реки Кумбель (это примерные данные)
kumbel_flood_coordinates = [51.6784, 39.2022]

# Создание карты с использованием координат центра павода
m = folium.Map(location=kumbel_flood_coordinates, zoom_start=12)

# Добавление маркера на карту для обозначения павода реки Кумбель
folium.Marker(
    location=kumbel_flood_coordinates,
    popup='Паводок реки Кумбель',
    icon=folium.Icon(color='red')
).add_to(m)

# Сохранение карты в HTML-файл
m.save("233.html")

print("Карта сохранена как 233.html")