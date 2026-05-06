import folium

# Координаты истоков рек (заменить на точные координаты)
source_ulken = [43.25, 76.90]
source_urzhar = [43.10, 77.80]

# Вычисление расстояния (приближенное)
from math import radians, cos, sin, acos, sqrt
def distance(lat1, lon1, lat2, lon2):
    R = 6371  # Радиус Земли в км
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    delta_phi = radians(lat2 - lat1)
    delta_lambda = radians(lon2 - lon1)

    a = sin(delta_phi / 2)**2 + cos(phi1) * cos(phi2) * sin(delta_lambda / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

distance_km = distance(source_ulken[0], source_ulken[1], source_urzhar[0], source_urzhar[1])

# Создание карты
m = folium.Map(location=[43.2, 77.5], zoom_start=8)

# Добавление точек истоков на карту
folium.Marker(location=source_ulken, popup="Исток Улькен Алматы").add_to(m)
folium.Marker(location=source_urzhar, popup="Исток Уржар").add_to(m)

# Добавление линии между точками
folium.PolyLine(locations=[source_ulken, source_urzhar], color='red').add_to(m)

# Сохранение карты
m.save("99.html")

print(f"Расстояние между истоками рек: {distance_km:.2f} км")