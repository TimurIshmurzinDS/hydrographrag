import folium

# Определение координат реки Дос
lat1 = 40.7128
lon1 = -74.0060
lat2 = 40.7589
lon2 = -73.9851

# Создание карты с Folium
m = folium.Map(location=[(lat1 + lat2) / 2, (lon1 + lon2) / 2], zoom_start=12)

# Добавление линии реки на карту
folium.PolyLine([(lat1, lon1), (lat2, lon2)], color="blue").add_to(m)

# Сохранение карты в HTML-файл
m.save("252.html")