import folium

# Шаг 1: Сбор данных
# Координаты истока реки Улькен Алматы (примерные значения)
istok_ulken_almaty = [42.8536, 79.0856]

# Координаты истока реки Уржар (примерные значения)
istok_urzar = [42.8183, 78.9850]

# Шаг 2: Подготовка данных
coordinates = {
    "Улькен Алматы": istok_ulken_almaty,
    "Уржар": istok_urzar
}

# Шаг 3: Визуализация на карте
# Создание карты с центром между двумя точками
center_map = [(istok_ulken_almaty[0] + istok_urzar[0]) / 2, (istok_ulken_almaty[1] + istok_urzar[1]) / 2]
m = folium.Map(location=center_map, zoom_start=11)

# Добавление маркеров на карту
for river, coord in coordinates.items():
    folium.Marker(
        location=coord,
        popup=f"Исток реки {river}",
        icon=folium.Icon(icon="info-sign")
    ).add_to(m)

# Шаг 4: Сохранение карты
m.save("99.html")

print("Карта сохранена как '99.html'")