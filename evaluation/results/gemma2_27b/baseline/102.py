import geopy.distance
import folium

# Координаты точек впадения (заменить на реальные координаты)
point_karatal = (43.2589, 76.9102)  
point_ulken_almaty = (43.2289, 76.9802)

# Расчет расстояния
distance = geopy.distance.geodesic(point_karatal, point_ulken_almaty).km

print("Расстояние между точками впадения рек:", distance, "км")

# Визуализация (необязательно)
m = folium.Map(location=[43.24, 76.95], zoom_start=12)
folium.Marker(location=point_karatal, popup="Впадение реки Каратал").add_to(m)
folium.Marker(location=point_ulken_almaty, popup="Впадение реки Улькен Алматы").add_to(m)

# Соединить точки линией
folium.PolyLine([point_karatal, point_ulken_almaty]).add_to(m)

m.save("102.html")