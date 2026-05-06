import folium
from math import radians, sin, cos, sqrt, atan2

# Координаты точек впадения реки Каратал и Улькен Алматы (предположим)
point_karatal = [43.1234, 76.5678]  # Latitude, Longitude
point_ulken_almaty = [42.9012, 76.4956]

# Функция для расчета расстояния между двумя точками на сфере (например, Земля)
def haversine_distance(point1, point2):
    lat1, lon1 = radians(point1[0]), radians(point1[1])
    lat2, lon2 = radians(point2[0]), radians(point2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Радиус Земли в километрах (предположим)
    R = 6371

    return R * c

# Расчет расстояния между точками
distance = haversine_distance(point_karatal, point_ulken_almaty)

print(f"Расстояние между точками впадения реки Каратал и Улькен Алматы: {distance} км")

# Визуализация на карте (если требуется)
m = folium.Map(location=[point_karatal[0], point_ulken_almaty[1]], zoom_start=10)

folium.Marker([point_karatal[0], point_karatal[1]], popup='Точка впадения реки Каратал').add_to(m)
folium.Marker([point_ulken_almaty[0], point_ulken_almaty[1]], popup='Точка впадения реки Улькен Алматы').add_to(m)

m.save("102.html")