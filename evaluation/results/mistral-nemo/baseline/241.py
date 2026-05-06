import folium
from geopy.distance import geodesic

# Географические координаты реки Талгар (43.2569° с. ш., 71.3806° в. д.)
talgar_river = (43.2569, 71.3806)

# Географические координаты Луны (0° с. ш., 0° з. д.)
moon = (0, 0)

# Вычисление расстояния между рекой Талгар и Луной
distance = geodesic(talgar_river, moon).km

print(f"Расстояние между рекой Талгар и Луной: {distance} км")

# Создание карты с местоположением реки Талгар и Луны
m = folium.Map(location=talgar_river, zoom_start=4)

folium.Marker(talgar_river, popup="Река Талгар").add_to(m)
folium.Marker(moon, popup="Луна").add_to(m)

# Сохранение карты в файл
m.save("241.html")