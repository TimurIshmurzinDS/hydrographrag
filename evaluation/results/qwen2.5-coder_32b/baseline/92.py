import folium
from geopy.distance import geodesic

# Координаты устья реки Дос (примерные значения)
mouth_of_dos = (43.1506, 78.0421)

# Координаты начала реки Емель (примерные значения)
source_of_emel = (43.9333, 78.5833)

# Вычисление расстояния между точками
distance = geodesic(mouth_of_dos, source_of_emel).kilometers

print(f"Расстояние между устьем реки Дос и началом реки Емель: {distance:.2f} км")

# Создание карты с использованием folium
m = folium.Map(location=[(mouth_of_dos[0] + source_of_emel[0]) / 2, (mouth_of_dos[1] + source_of_emel[1]) / 2], zoom_start=9)

# Добавление маркеров для устья реки Дос и начала реки Емель
folium.Marker(mouth_of_dos, popup='Устье реки Дос').add_to(m)
folium.Marker(source_of_emel, popup='Начало реки Емель').add_to(m)

# Добавление линии между точками
folium.PolyLine([mouth_of_dos, source_of_emel], color="blue", weight=2.5, opacity=1).add_to(m)

# Сохранение карты в файл 92.html
m.save("92.html")