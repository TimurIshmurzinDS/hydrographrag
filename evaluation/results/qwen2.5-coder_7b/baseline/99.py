import folium

# Географические координаты истоков рек
source_ulken_almaty = (43.2167, 76.9500)  # Примерные координаты истока реки Улькен Алматы
source_urzhar = (43.1833, 76.9333)      # Примерные координаты истока реки Уржар

# Создание карты с центром между источниками рек
m = folium.Map(location=[(source_ulken_almaty[0] + source_urzhar[0]) / 2, 
                         (source_ulken_almaty[1] + source_urzhar[1]) / 2], zoom_start=13)

# Добавление маркеров для истоков рек
folium.Marker(source_ulken_almaty, popup='Исток реки Улькен Алматы', icon=folium.Icon(color='red')).add_to(m)
folium.Marker(source_urzhar, popup='Исток реки Уржар', icon=folium.Icon(color='blue')).add_to(m)

# Сохранение карты
m.save("99.html")

print(f"Координаты истока реки Улькен Алматы: {source_ulken_almaty}")
print(f"Координаты истока реки Уржар: {source_urzhar}")

# Расчет расстояния между источниками рек
from geopy.distance import geodesic

distance = geodesic(source_ulken_almaty, source_urzhar).kilometers
print(f"Расстояние между источниками реки Улькен Алматы и реки Уржар: {distance:.2f} километров")