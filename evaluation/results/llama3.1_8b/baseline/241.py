import folium

# Координаты реки Талгар (предположительно)
talgar_coords = [42.7333, 76.9833]

# Координаты Луны (центр)
moon_coords = [0, 0]  # В действительности координаты Луны не имеют смысла в географическом контексте

# Создание карты
m = folium.Map(location=talgar_coords, zoom_start=10)

# Добавление маркера для реки Талгар
folium.Marker(talgar_coords, popup='Река Талгар').add_to(m)

# Добавление маркера для Луны (предположительно)
folium.Marker(moon_coords, popup='Луна', icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("241.html")