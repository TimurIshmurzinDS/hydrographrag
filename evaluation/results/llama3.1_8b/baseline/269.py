import folium

# Создаем карту Луны
moon_map = folium.Map(location=[-23.4, 17.5], zoom_start=10)

# Добавляем маркер фермы на Луне
folium.Marker([-23.4, 17.5], popup='Ферма на Луне').add_to(moon_map)

# Добавляем слой для системы орошения
folium.GeoJson(
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "LineString", "coordinates": [[-23.4, 17.5], [-23.6, 18.2]]},
                "properties": {"name": "Река Киши Осек"},
            }
        ],
    },
).add_to(moon_map)

# Добавляем слой для защиты растений
folium.GeoJson(
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Polygon", "coordinates": [[[-23.4, 17.5], [-23.6, 18.2], [-24.1, 19.3], [-23.4, 17.5]]]},
                "properties": {"name": "Защита растений"},
            }
        ],
    },
).add_to(moon_map)

# Сохраняем карту в файл
moon_map.save("269.html")