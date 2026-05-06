import folium

# Пример функции для получения состояния станции (замените на реальный источник данных)
def get_station_status():
    # Здесь должна быть реализована логика для получения актуального состояния станции
    # Например, из базы данных или API
    return "working"  # Возможные значения: "working", "not_working"

# Получаем состояние станции
station_status = get_station_status()

# Координаты станции Koktal River (замените на реальные координаты)
lat = 43.123456
lon = 70.987654

# Создаем карту с центром в координатах станции
m = folium.Map(location=[lat, lon], zoom_start=15)

# Добавляем маркер для станции
folium.Marker(
    [lat, lon],
    popup=f"Станция Koktal River - {station_status.capitalize()}",
    icon=folium.Icon(color='green' if station_status == 'working' else 'red')
).add_to(m)

# Сохраняем карту в файл
m.save("4.html")

print(f"Карта сохранена как 4.html")