import folium

# Создание карты с центром над рекой Karaoy River
m = folium.Map(location=[40.7128, 43.9338], zoom_start=13)

# Добавление точек телепортации на карту (в данном примере используются произвольные координаты)
teleportation_points = [(40.72, 43.95), (40.69, 43.92), (40.71, 43.94)]
for point in teleportation_points:
    folium.Marker(point).add_to(m)

# Сохранение карты как "216.html"
m.save("216.html")