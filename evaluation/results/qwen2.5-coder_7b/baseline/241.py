import folium
from geopy.distance import geodesic

# Координаты реки Талгар (пример, нужно заменить реальными координатами)
talgar_coords = (43.123456, 70.987654)  # Примерные координаты, нужно обновить

# Координаты Луны (пример, нужно заменить реальными координатами)
moon_coords = (23.456789, -120.987654)  # Примерные координаты, нужно обновить

# Расчет расстояния между рекой Талгар и Луной
distance_km = geodesic(talgar_coords, moon_coords).kilometers
print(f"Расстояние между рекой Талгар и Луной: {distance_km:.2f} километров")

# Создание карты с отметками
m = folium.Map(location=[(talgar_coords[0] + moon_coords[0]) / 2, (talgar_coords[1] + moon_coords[1]) / 2], zoom_start=5)

# Добавление маркеров для реки Талгар и Луны
folium.Marker(talgar_coords, popup='Река Талгар', icon=folium.Icon(color='blue')).add_to(m)
folium.Marker(moon_coords, popup='Луна', icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("241.html")