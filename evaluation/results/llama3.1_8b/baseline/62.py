import folium
from folium.plugins import TimestampedGeoJson

# Данные о постах мониторинга (примерные данные)
posts_data = {
    "post1": {"location": [48.5, 69.2], "status": "working"},
    "post2": {"location": [49.0, 68.8], "status": "not working"},
    "post3": {"location": [47.9, 70.1], "status": "working"}
}

# Данные о реке Sharyn River (примерные данные)
river_data = {
    "type": "Feature",
    "geometry": {
        "type": "LineString",
        "coordinates": [[68.8, 48.5], [69.2, 49.0], [70.1, 47.9]]
    }
}

# Создаем карту
m = folium.Map(location=[48.75, 69.5], zoom_start=10)

# Добавляем маркеры для постов мониторинга
for post_name, post_data in posts_data.items():
    if post_data["status"] == "not working":
        folium.Marker(post_data["location"], popup=f"{post_name} - не работает").add_to(m)
    else:
        folium.Marker(post_data["location"], popup=f"{post_name} - работает").add_to(m)

# Добавляем линию реки Sharyn River
folium.PolyLine(river_data["geometry"]["coordinates"]).add_to(m)

# Сохраняем карту в файл
m.save("62.html")