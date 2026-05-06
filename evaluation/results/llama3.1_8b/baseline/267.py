import folium

# Широта и долгота реки Баскан (примерные значения)
latitude = 43.1234
longitude = -2.3456

# Создание карты
m = folium.Map(location=[latitude, longitude], zoom_start=10)

# Добавление маркера на карте для реки Баскан
folium.Marker([latitude, longitude], popup='Река Баскан').add_to(m)

# Определение оптимального места сбора льда (примерное значение)
optimal_latitude = 43.1234 + 0.01
optimal_longitude = -2.3456 + 0.02

# Добавление маркера на карте для оптимального места сбора льда
folium.Marker([optimal_latitude, optimal_longitude], popup='Оптимальное место сбора льда').add_to(m)

# Сохранение карты в файл
m.save("267.html")