import folium

# Создание карты с центром в районе Луны
m = folium.Map(location=[0, 0], zoom_start=4)

# Добавление маркера для фермы
farm_location = [2.5, -179]  # Примерные координаты на Луне (в градусах)
folium.Marker(farm_location, popup='Ферма', icon=folium.Icon(color='green')).add_to(m)

# Добавление маркера для системы орошения
irrigation_system_location = [2.5, -178]  # Примерные координаты на Луне (в градусах)
folium.Marker(irrigation_system_location, popup='Система орошения', icon=folium.Icon(color='blue')).add_to(m)

# Сохранение карты
m.save("269.html")