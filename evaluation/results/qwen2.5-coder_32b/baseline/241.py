import math
from geopy.distance import geodesic
import folium

# Координаты реки Талгар (примерные координаты, так как точное местоположение может отличаться)
coordinates_talgar = (42.8506, 79.1343)

# Координаты Луны в географической системе отсчёта Земли (примерные координаты для ближайшей точки Луны к Земле)
# На самом деле Луна движется по эллиптической орбите, но для простоты возьмём средние координаты
coordinates_moon = (0, 0)  # Луна находится примерно над экватором Земли

# Расчет расстояния между рекой Талгар и Луной с использованием геодезической формулы
distance_km = geodesic(coordinates_talgar, coordinates_moon).kilometers

# Вывод результата
print(f"Расстояние между рекой Талгар и Луной: {distance_km} км")

# Создание карты с помощью folium
m = folium.Map(location=coordinates_talgar, zoom_start=5)

# Добавление маркера для реки Талгар
folium.Marker(coordinates_talgar, popup='Река Талгар').add_to(m)

# Добавление маркера для Луны (на самом деле Луна не находится на поверхности Земли)
folium.Marker(coordinates_moon, popup='Луна').add_to(m)

# Сохранение карты в файл
m.save("241.html")