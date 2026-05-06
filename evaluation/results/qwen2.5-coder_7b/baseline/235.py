import folium

# Координаты спутника и точки запуска
satellite_coords = (52.3702, 4.8952)  # Пример координат спутника
launch_point_coords = (51.5074, -0.1278)  # Пример координат точки запуска

# Создание карты
m = folium.Map(location=[(satellite_coords[0] + launch_point_coords[0]) / 2, 
                         (satellite_coords[1] + launch_point_coords[1]) / 2], zoom_start=5)

# Добавление маркера для спутника
folium.Marker(satellite_coords, popup='Спутник', icon=folium.Icon(color='red')).add_to(m)

# Добавление маркера для точки запуска
folium.Marker(launch_point_coords, popup='Точка запуска', icon=folium.Icon(color='blue')).add_to(m)

# Сохранение карты в HTML файл
m.save("235.html")