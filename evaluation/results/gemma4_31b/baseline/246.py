import folium
import math

def haversine(coord1, coord2):
    """
    Вычисляет расстояние между двумя точками на сфере (в километрах).
    """
    R = 6371.0  # Радиус Земли в км
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def main():
    # 1. Координаты объектов
    # Орион (подзвездная точка центра созвездия: экватор, ~88.75 в.д.)
    orion_coords = [0.0, 88.75] 
    # Река Шилик (примерная точка в Восточном Казахстане)
    shilik_coords = [48.5, 80.5]

    # 2. Расчет расстояния
    distance = haversine(orion_coords, shilik_coords)
    print(f"Кратчайшее расстояние (ортодромия): {distance:.2f} км")

    # 3. Создание карты
    # Центрируем карту между двумя точками
    center_lat = (orion_coords[0] + shilik_coords[0]) / 2
    center_lon = (orion_coords[1] + shilik_coords[1]) / 2
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=3, control_scale=True)

    # Добавление маркера для Ориона
    folium.Marker(
        location=orion_coords,
        popup=f"Подзвездная точка Ориона\nРасстояние: {distance:.2f} км",
        tooltip="Созвездие Ориона (Проекция)",
        icon=folium.Icon(color='blue', icon='star')
    ).add_to(m)

    # Добавление маркера для реки Шилик
    folium.Marker(
        location=shilik_coords,
        popup="Река Шилик (Казахстан)",
        tooltip="Река Шилик",
        icon=folium.Icon(color='green', icon='tint')
    ).add_to(m)

    # 4. Отрисовка кратчайшего пути (линия между точками)
    path_coords = [orion_coords, shilik_coords]
    folium.PolyLine(
        locations=path_coords,
        color='red',
        weight=3,
        opacity=0.8,
        tooltip="Кратчайший путь"
    ).add_to(m)

    # Сохранение карты
    m.save("246.html")
    print("Карта успешно сохранена в файл 246.html")

if __name__ == "__main__":
    main()