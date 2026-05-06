import folium

# Создаем карту с центром в Каскелене
m = folium.Map(location=[54.3276, -1.0819], zoom_start=10)

# Добавляем маркер для реки Каскелен
folium.Marker([54.3276, -1.0819], popup='Каскелен').add_to(m)

# Сохраняем карту
m.save("232.html")