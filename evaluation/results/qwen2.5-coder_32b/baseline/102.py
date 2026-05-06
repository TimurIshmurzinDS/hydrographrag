import folium
from geopy.distance import geodesic

# Координаты точек впадения рек (широта, долгота)
coordinates_karatag = (42.853611, 79.033889)  # Примерные координаты для Каратал
coordinates_ulkent_almaty = (42.853611, 79.033889)  # Примерные координаты для Улькен Алматы

# Расчет расстояния между точками впадения рек
distance = geodesic(coordinates_karatag, coordinates_ulkent_almaty).kilometers
print(f"Расстояние между точками впадения рек Каратал и Улькен Алматы: {distance:.2f} км")

# Создание интерактивной карты с помощью folium
m = folium.Map(location=[(coordinates_karatag[0] + coordinates_ulkent_almaty[0]) / 2,
                         (coordinates_karatag[1] + coordinates_ulkent_almaty[1]) / 2],
               zoom_start=10)

# Добавление маркеров для точек впадения рек
folium.Marker(coordinates_karatag, popup='Каратал').add_to(m)
folium.Marker(coordinates_ulkent_almaty, popup='Улькен Алматы').add_to(m)

# Добавление линии между точками
folium.PolyLine([coordinates_karatag, coordinates_ulkent_almaty], color="blue", weight=2.5, opacity=1).add_to(m)

# Сохранение карты в файл
m.save("102.html")