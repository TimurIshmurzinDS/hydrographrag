import geopy.distance
from geopy.geocoders import Nominatim

# Инициализируем провайдера геолокации
geolocator = Nominatim(user_agent="geoapiExercises")

# Получаем координаты истока реки Улькен Алматы
ulken_almaty = geolocator.geocode("Устье реки Улькен Алматы")
ulken_almaty_coords = (ulken_almaty.latitude, ulken_almaty.longitude)

# Получаем координаты истока реки Уржар
urjar = geolocator.geocode("Исток реки Уржар")
urjar_coords = (urjar.latitude, urjar.longitude)

# Сравниваем координаты
if ulken_almaty_coords != urjar_coords:
    # Если координаты различаются, создаем карту и отмечаем на ней истоки рек
    m = folium.Map(location=[(ulken_almaty.latitude + urjar.latitude) / 2, (ulken_almaty.longitude + urjar.longitude) / 2], zoom_start=10)

    folium.Marker([ulken_almaty.latitude, ulken_almaty.longitude], popup="Устье реки Улькен Алматы").add_to(m)
    folium.Marker([urjar.latitude, urjar.longitude], popup="Исток реки Уржар").add_to(m)

    # Сохраняем карту как "99.html"
    m.save("99.html")
else:
    print("Координаты истока реки Улькен Алматы и реки Уржар совпадают.")