import folium
from geopy.distance import geodesic

def solve_gis_task():
    # 1. Координаты истоков рек (приблизительные значения для моделирования)
    # Река Большой Алматы (Ulken Almaty) - Заилийский Алатау
    river_almaty = {
        "name": "Исток реки Большой Алматы",
        "coords": (43.2250, 76.9120) 
    }
    
    # Река Уржар - Восточный Казахстан
    river_urzhar = {
        "name": "Исток реки Уржар",
        "coords": (49.5510, 82.6150)
    }

    # 2. Сравнительный анализ
    lat1, lon1 = river_almaty["coords"]
    lat2, lon2 = river_urzhar["coords"]

    # Расчет расстояния с помощью geopy (использует эллипсоид WGS-84)
    distance = geodesic(river_almaty["coords"], river_urzhar["coords"]).kilometers

    # Определение относительного положения
    lat_diff = lat2 - lat1
    lon_diff = lon2 - lon1

    print(f"--- Сравнение координат ---")
    print(f"{river_almaty['name']}: {lat1}, {lon1}")
    print(f"{river_urzhar['name']}: {lat2}, {lon2}")
    print(f"Расстояние между истоками: {distance:.2f} км")
    
    if lat_diff > 0:
        print(f"Река Уржар находится севернее реки Большой Алматы на {abs(lat_diff):.2f} градуса.")
    else:
        print(f"Река Большой Алматы находится севернее реки Уржар на {abs(lat_diff):.2f} градуса.")

    if lon_diff > 0:
        print(f"Река Уржар находится восточнее реки Большой Алматы на {abs(lon_diff):.2f} градуса.")
    else:
        print(f"Река Большой Алматы находится восточнее реки Уржар на {abs(lon_diff):.2f} градуса.")

    # 3. Визуализация на карте
    # Центрируем карту между двумя точками
    center_lat = (lat1 + lat2) / 2
    center_lon = (lon1 + lon2) / 2
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=5, control_scale=True)

    # Добавление маркеров
    folium.Marker(
        location=river_almaty["coords"],
        popup=f"{river_almaty['name']}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

    folium.Marker(
        location=river_urzhar["coords"],
        popup=f"{river_urzhar['name']}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

    # Линия между точками
    folium.PolyLine(
        locations=[river_almaty["coords"], river_urzhar["coords"]],
        color='green',
        weight=2.5,
        opacity=0.8,
        tooltip=f"Расстояние: {distance:.2f} км"
    ).add_to(m)

    # 4. Сохранение карты
    m.save("99.html")
    print("\nКарта успешно сохранена в файл 99.html")

if __name__ == "__main__":
    solve_gis_task()