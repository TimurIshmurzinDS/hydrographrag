import folium

def calculate_distance_to_moon():
    # 1. Координаты реки Талгар (приблизительный центр)
    # Широта: ~43.1, Долгота: ~77.5 (Казахстан)
    talgar_coords = [43.1, 77.5]
    location_name = "Река Талгар"

    # 2. Среднее расстояние от Земли до Луны в километрах
    # Среднее расстояние (полуось большой оси эллипса)
    avg_distance_earth_moon_km = 384400 

    # 3. Расчет
    # Поскольку Луна находится в космическом пространстве, 
    # расстояние от конкретной точки на поверхности Земли до Луны 
    # в среднем равно расстоянию от Земли до Луны.
    distance = avg_distance_earth_moon_km

    print(f"Объект: {location_name}")
    print(f"Координаты: {talgar_coords}")
    print(f"Среднее расстояние до Луны: {distance:,} км")

    # 4. Визуализация на карте
    # Создаем карту, центрированную на реке Талгар
    m = folium.Map(location=talgar_coords, zoom_start=8)

    # Добавляем маркер для реки Талгар
    folium.Marker(
        location=talgar_coords,
        popup=f"{location_name}\nРасстояние до Луны: ~{distance:,} км",
        tooltip=location_name,
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

    # Сохранение карты строго в файл 241.html
    m.save("241.html")
    print("Карта сохранена в файл 241.html")

if __name__ == "__main__":
    calculate_distance_to_moon()