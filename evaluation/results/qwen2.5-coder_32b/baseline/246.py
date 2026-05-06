import folium
from geopy.distance import geodesic

# Координаты центра созвездия Ориона (примерные)
orion_coords = (7.65, 89.21)

# Координаты точки на реке Шилик (примерные)
shiliq_coords = (43.03, 77.59)

# Расчет геодезического расстояния между точками
distance = geodesic(orion_coords, shiliq_coords).kilometers

print(f"Расстояние между созвездием Ориона и рекой Шилик: {distance:.2f} км")

# Создание карты folium
m = folium.Map(location=[(orion_coords[0] + shiliq_coords[0]) / 2, (orion_coords[1] + shiliq_coords[1]) / 2], zoom_start=4)

# Добавление маркеров для созвездия Ориона и реки Шилик
folium.Marker(
    location=orion_coords,
    popup='Созвездие Орион',
    icon=folium.Icon(color='blue')
).add_to(m)

folium.Marker(
    location=shiliq_coords,
    popup='Река Шилик',
    icon=folium.Icon(color='green')
).add_to(m)

# Добавление линии между точками
folium.PolyLine([orion_coords, shiliq_coords], color="red", weight=2.5, opacity=1).add_to(m)

# Сохранение карты в файл
m.save("246.html")