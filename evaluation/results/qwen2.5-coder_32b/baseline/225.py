import folium

# Координаты примерного центра реки Кыши Алматы (это приближенные координаты)
center_coordinates = [42.8650, 76.9130]

# Создание карты с использованием folium
m = folium.Map(location=center_coordinates, zoom_start=12)

# Добавление линии, представляющей маршрут реки Кыши Алматы (примерные координаты)
river_coordinates = [
    [42.8650, 76.9130],
    [42.8640, 76.9140],
    [42.8630, 76.9150],
    # Добавьте больше точек для более точного представления маршрута реки
]

folium.PolyLine(river_coordinates, color="blue", weight=2.5, opacity=1).add_to(m)

# Сохранение карты в файл
m.save("225.html")