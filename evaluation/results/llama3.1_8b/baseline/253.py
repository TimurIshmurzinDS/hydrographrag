import folium

# Координаты Альфы Центавра (предположим, что они известны)
alfa_centauri_coords = [-62.6869, 47.8667]

# Широта точки на реке Караой (предположим, что она известна)
karakoy_river_coords = [42.7333, 70.2833]

# Создаем карту
m = folium.Map(location=karakoy_river_coords, zoom_start=10)

# Добавляем маркер для Альфы Центавра на карте
folium.Marker(alfa_centauri_coords, popup='Альфа Центавра').add_to(m)

# Рассчитываем расстояние между двумя точками (предположим, что широта точки на реке Караой является приближенным значением расстояния)
distance = abs(karakoy_river_coords[0] - alfa_centauri_coords[0])

# Добавляем информацию о расстоянии на карту
folium.Marker([karakoy_river_coords[0], alfa_centauri_coords[1]], popup=f'Расстояние до Альфы Центавра: {distance} градусов').add_to(m)

# Сохраняем карту в файл
m.save("253.html")