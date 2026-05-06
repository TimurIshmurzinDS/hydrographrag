import folium

# Координаты реки Эмел (примерные координаты)
emel_coords = [43.2067, 131.8958]

# Создание объекта карты с центром в месте реки Эмел
m = folium.Map(location=emel_coords, zoom_start=10)

# Добавление маркера на место предполагаемого происшествия
folium.Marker(
    location=[43.2067, 131.8958],
    popup='Катастрофа на реке Эмел',
    icon=folium.Icon(color='red')
).add_to(m)

# Добавление круга вокруг маркера для показа области воздействия катастрофы
folium.Circle(
    location=[43.2067, 131.8958],
    radius=5000,  # Радиус в метрах
    color='red',
    fill=True,
    fill_color='crimson'
).add_to(m)

# Сохранение карты в файл HTML
m.save("265.html")