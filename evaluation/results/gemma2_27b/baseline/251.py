import folium

# Создаем карту с центром на реке Кумбель (координаты)
m = folium.Map(location=[42.5, 60], zoom_start=10)

# Добавляем линию для "реки"
folium.PolyLine([(42.5, 60), (42.6, 60.1)], color='blue', weight=3).add_to(m)

# Добавляем линии для "притоков"
folium.PolyLine([(42.55, 60.05), (42.5, 60.1)], color='darkblue', weight=2).add_to(m)
folium.PolyLine([(42.65, 60.15), (42.7, 60.2)], color='darkblue', weight=2).add_to(m)

# Сохраняем карту
m.save("251.html")