import folium

# Загрузка данных о станциях мониторинга
stations = {
    "Коктал": {"lat": 43.123456, "lon": 77.654321, "status": True},
    "Аксу": {"lat": 42.987654, "lon": 78.012345, "status": False}
}

# Определение текущего положения станции мониторинга
current_station = stations["Коктал"]

# Проверка, работает ли сейчас станция мониторинга
if current_station["status"]:
    status_text = "Работает"
else:
    status_text = "Не работает"

# Создание карты
m = folium.Map(location=[current_station["lat"], current_station["lon"]], zoom_start=10)

# Добавление маркера на карте
folium.Marker([current_station["lat"], current_station["lon"]], popup=status_text).add_to(m)

# Визуализация результата на карте
m.save("4.html")