import math

# Координаты реки Талгар (примерные)
x1 = 43.25
y1 = 76.95
z1 = 0 # Уровень моря

# Среднее расстояние от Земли до Луны
x2 = 0
y2 = 0
z2 = 384400000  # В метрах

# Расчет расстояния
distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

print(f"Расстояние между рекой Талгар и Луной: {distance} метров")

# Визуализация (необязательно)
import folium

m = folium.Map(location=[43.25, 76.95], zoom_start=10)
folium.Marker([x1, y1]).add_to(m)
folium.Marker([0, 0]).add_to(m)
m.save("241.html")