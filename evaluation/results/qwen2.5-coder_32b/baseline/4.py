import folium

# Предположим, что у нас есть данные о станции мониторинга в формате словаря
monitoring_station = {
    "name": "Станция мониторинга на реке Koktal River",
    "coordinates": [42.874365, 74.590113],  # Примерные координаты станции
    "status": "active"  # Состояние станции: 'active' или 'inactive'
}

# Создание карты с центром в месте станции мониторинга
m = folium.Map(location=monitoring_station["coordinates"], zoom_start=12)

# Добавление маркера на карту с информацией о станции
popup_text = f"Название: {monitoring_station['name']}<br>Статус: {monitoring_station['status']}"
folium.Marker(
    location=monitoring_station["coordinates"],
    popup=popup_text,
    icon=folium.Icon(color='green' if monitoring_station['status'] == 'active' else 'red')
).add_to(m)

# Сохранение карты в файл HTML
m.save("4.html")

print(f"Станция мониторинга на реке Koktal River {'работает' if monitoring_station['status'] == 'active' else 'не работает'}")