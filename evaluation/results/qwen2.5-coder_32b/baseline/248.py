import folium

# Координаты реки Аксу (примерные)
aksu_coords = [42.8516, 79.0349]

# Примерные координаты области на Марсе для колонизации (например, Нильский дельта)
mars_colony_coords = [-1.9462, 247.6251]

# Создание карты с центром в выбранной области на Марсе
m = folium.Map(location=mars_colony_coords, zoom_start=8)

# Добавление маркера для реки Аксу (для сравнения)
folium.Marker(
    location=aksu_coords,
    popup='Река Аксу',
    icon=folium.Icon(color='blue')
).add_to(m)

# Добавление маркера для области колонизации на Марсе
folium.Marker(
    location=mars_colony_coords,
    popup='Область для колонизации на Марсе',
    icon=folium.Icon(color='red')
).add_to(m)

# Сохранение карты в файл
m.save("248.html")