import folium

# Координаты реки Талгар (предположительно)
lat = 42.933333
lon = 76.983333

# Создание карты
m = folium.Map(location=[lat, lon], zoom_start=10)

# Добавление маркера в точку, соответствующую реке Талгар
folium.Marker([lat, lon], popup='Река Талгар').add_to(m)

# Сохранение карты как HTML-файл
m.save("256.html")