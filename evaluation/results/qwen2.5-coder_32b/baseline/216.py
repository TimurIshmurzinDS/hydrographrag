import folium

# Пример данных: координаты сенсоров реки Karaoy River (широта, долгота)
sensor_data = [
    (43.0758, 79.8557),
    (43.1234, 79.9012),
    (43.0567, 79.8890),
    (43.1012, 79.8765)
]

# Определяем оптимальные точки для телепортации (например, берем первые две точки из данных)
teleport_points = sensor_data[:2]

# Создаем карту с центром в средней точке всех сенсоров
center_lat = sum(lat for lat, lon in sensor_data) / len(sensor_data)
center_lon = sum(lon for lat, lon in sensor_data) / len(sensor_data)

m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# Добавляем маркеры для сенсоров
for lat, lon in sensor_data:
    folium.Marker([lat, lon], popup='Сенсор').add_to(m)

# Добавляем маркеры для точек телепортации
for i, (lat, lon) in enumerate(teleport_points):
    folium.Marker([lat, lon], popup=f'Точка телепортации {i+1}', icon=folium.Icon(color='green')).add_to(m)

# Сохраняем карту в файл 216.html
m.save("216.html")