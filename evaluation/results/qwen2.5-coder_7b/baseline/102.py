import folium
from geopy.distance import geodesic

# Координаты точек впадения рек
karatalka_coords = (43.2167, 76.9500)  # Пример координат для Каратал
ulken_almaty_coords = (43.2200, 76.9600)  # Пример координат для Улькен Алматы

# Вычисление расстояния между точками
distance_km = geodesic(karatalka_coords, ulken_almaty_coords).kilometers
print(f"Расстояние между точками впадения реки Каратал и Улькен Алматы: {distance_km:.2f} км")

# Создание карты с точками и расстоянием
m = folium.Map(location=[(karatalka_coords[0] + ulken_almaty_coords[0]) / 2, (karatalka_coords[1] + ulken_almaty_coords[1]) / 2], zoom_start=14)

# Добавление точек на карту
folium.Marker(karatalka_coords, popup='Каратал', icon=folium.Icon(color='red')).add_to(m)
folium.Marker(ulken_almaty_coords, popup='Улькен Алматы', icon=folium.Icon(color='blue')).add_to(m)

# Добавление линии между точками
folium.PolyLine([karatalka_coords, ulken_almaty_coords], color='green', weight=2.5, opacity=1).add_to(m)

# Сохранение карты
m.save("102.html")