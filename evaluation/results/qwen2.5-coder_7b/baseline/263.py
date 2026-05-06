import folium

# Создаем карту с центром в реке Талгар
m = folium.Map(location=[43.0725, 76.9183], zoom_start=12)

# Добавляем маркер для реки Талгар
folium.Marker(
    [43.0725, 76.9183],
    popup='Река Талгар',
    icon=folium.Icon(color='blue', icon='water')
).add_to(m)

# Добавляем маркер для искусственной среды выращивания картофеля
folium.Marker(
    [43.0725, 76.9183],
    popup='Искусственная среда для выращивания картофеля',
    icon=folium.Icon(color='green', icon='leaf')
).add_to(m)

# Сохраняем карту
m.save("263.html")