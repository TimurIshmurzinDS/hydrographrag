import folium

# Координаты устья реки Дос (предположим)
uos = [55.1234, 61.9876]

# Координаты начала реки Емель (предположим)
nre = [52.3456, 63.4567]

# Создаем карту
m = folium.Map(location=[uos[0], nre[1]], zoom_start=10)

# Добавляем маркеры для устья и начала реки
folium.Marker([uos[0], uos[1]], popup='Устье реки Дос').add_to(m)
folium.Marker([nre[0], nre[1]], popup='Начало реки Емель').add_to(m)

# Вычисляем расстояние между устьем и началом
distance = folium.plugins.AntPath([[uos[0], uos[1]], [nre[0], nre[1]]]).add_to(m)
folium.Marker([uos[0] + (nre[0]-uos[0])/2, uos[1] + (nre[1]-uos[1])/2], popup=f'Расстояние: {distance.get_distance()} км').add_to(m)

# Сохраняем карту
m.save("92.html")