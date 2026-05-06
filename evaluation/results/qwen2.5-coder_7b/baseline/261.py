import folium
from folium.plugins import MarkerCluster

# Данные о местоположении реки Киши Осек и точках для засолки овощей
kishi_osak_location = (51.6094, 37.2823)  # Примерные координаты реки Киши Осек
vegetable_locations = [
    (51.6100, 37.2830),
    (51.6095, 37.2840),
    (51.6090, 37.2850)
]

# Создание карты
m = folium.Map(location=kishi_osak_location, zoom_start=15)

# Добавление маркера для реки Киши Осек
folium.Marker(kishi_osak_location, popup='Река Киши Осек', icon=folium.Icon(color='blue')).add_to(m)

# Добавление маркеров для точек засолки овощей
marker_cluster = MarkerCluster().add_to(m)
for loc in vegetable_locations:
    folium.Marker(loc, popup='Точка засолки овощей', icon=folium.Icon(color='green')).add_to(marker_cluster)

# Сохранение карты
m.save("261.html")

print("Карта сохранена как 261.html")