import folium

# Координаты рек (предположим, что они хранятся в базе данных)
river_coords = {
    'Уржар': [56.2333, 60.7333],
    'Дос': [54.6667, 62.3667],
    'Каратал': [45.2833, 74.7833]
}

# Создаем карту
m = folium.Map(location=[river_coords['Уржар'][0], river_coords['Уржар'][1]], zoom_start=10)

# Добавляем маркеры на местах рек
for name, coords in river_coords.items():
    folium.Marker(coords, popup=name).add_to(m)

# Сохраняем карту как HTML-файл
m.save("103.html")