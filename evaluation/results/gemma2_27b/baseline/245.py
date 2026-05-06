import geopy.distance
from geopy.geocoders import Nominatim

# 1. Поиск координат начала и конца реки
geolocator = Nominatim(user_agent="river_length")
start_coords = geolocator.geocode("начало реки Караой").point
end_coords = geolocator.geocode("конец реки Караой").point

# 2. Расчет длины реки
distance = geopy.distance.geodesic(start_coords, end_coords).km

print(f"Длина реки Караой: {distance:.2f} км")

# 3. Визуализация (невозможно вычислить массу черной дыры)
import folium

m = folium.Map(location=[start_coords.latitude, start_coords.longitude], zoom_start=8)
folium.Marker(location=[start_coords.latitude, start_coords.longitude], popup="Начало реки").add_to(m)
folium.Marker(location=[end_coords.latitude, end_coords.longitude], popup="Конец реки").add_to(m)

m.save("245.html")