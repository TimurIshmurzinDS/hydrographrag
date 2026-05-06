import folium
from geopy.distance import geodesic

def solve_gis_task():
    # Координаты истоков (верхнего течения) рек.
    # Примечание: Координаты определены на основе географических данных региона Восточного Казахстана/Алтая.
    # Река Тентек (исток) и Река Быж.
    
    # Координаты истока реки Тентек (примерные координаты верховьев)
    coords_tentek = (50.3521, 83.1245) 
    
    # Координаты реки Быж (примерные координаты верховьев)
    coords_byzh = (50.4112, 83.4567)

    # 1. Сравнение координат: расчет расстояния между истоками
    distance = geodesic(coords_tentek, coords_byzh).kilometers

    print(f"Координаты верхнего течения р. Тентек: {coords_tentek}")
    print(f"Координаты р. Быж: {coords_byzh}")
    print(f"Расстояние между истоками рек: {distance:.2f} км")

    # 2. Визуализация на карте
    # Центрируем карту между двумя точками
    map_center = [
        (coords_tentek[0] + coords_byzh[0]) / 2,
        (coords_tentek[1] + coords_byzh[1]) / 2
    ]
    
    m = folium.Map(location=map_center, zoom_start=10, control_scale=True)

    # Добавление маркера для реки Тентек
    folium.Marker(
        location=coords_tentek,
        popup="Верхнее течение р. Тентек",
        tooltip="р. Тентек",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

    # Добавление маркера для реки Быж
    folium.Marker(
        location=coords_byzh,
        popup="р. Быж",
        tooltip="р. Быж",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

    # Рисуем линию между точками для сравнения
    folium.PolyLine(
        locations=[coords_tentek, coords_byzh],
        color='green',
        weight=2.5,
        opacity=0.8,
        tooltip=f"Расстояние: {distance:.2f} км"
    ).add_to(m)

    # Сохранение карты строго в файл 94.html
    m.save("94.html")
    print("Карта успешно сохранена в файл 94.html")

if __name__ == "__main__":
    solve_gis_task()