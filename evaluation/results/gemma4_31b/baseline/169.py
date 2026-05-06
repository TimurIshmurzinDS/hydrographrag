import folium
from shapely.geometry import LineString, Point

def solve_river_intersection():
    # 1. Имитация координат русел рек (в реальном проекте здесь загрузка из GeoJSON/Shapefile)
    # Координаты представлены в формате (долгота, широта) для shapely
    # Река Талгар (условный путь)
    coords_talgar = [
        (77.35, 43.10), (77.40, 43.15), (77.45, 43.20), 
        (77.50, 43.25), (77.55, 43.30), (77.60, 43.35)
    ]
    
    # Река Шынжалы (условный путь, пересекающий Талгар)
    coords_shynzhaly = [
        (77.40, 43.10), (77.45, 43.15), (77.50, 43.20), 
        (77.55, 43.25), (77.60, 43.30)
    ]

    # 2. Создание объектов LineString
    line_talgar = LineString(coords_talgar)
    line_shynzhaly = LineString(coords_shynzhaly)

    # 3. Определение пространственного пересечения
    intersection = line_talgar.intersection(line_shynzhaly)

    # 4. Обработка результата пересечения
    intersection_point = None
    if intersection.is_empty:
        print("Пересечение не найдено.")
    elif isinstance(intersection, Point):
        intersection_point = (intersection.y, intersection.x)
        print(f"Точка пересечения найдена: {intersection_point}")
    elif intersection.geom_type == 'MultiPoint':
        # Если точек несколько, берем первую
        first_point = intersection.geoms[0]
        intersection_point = (first_point.y, first_point.x)
        print(f"Найдено несколько точек пересечения. Первая: {intersection_point}")
    elif intersection.geom_type == 'LineString':
        # Если реки сливаются на определенном участке
        print("Реки сливаются на определенном участке (пересечение является линией).")
        # Для визуализации возьмем центр этого участка
        centroid = intersection.centroid
        intersection_point = (centroid.y, centroid.x)

    # 5. Визуализация с помощью folium
    # Центрируем карту по одной из рек
    m = folium.Map(location=[43.20, 77.45], zoom_start=11, tiles='OpenStreetMap')

    # Добавляем русло реки Талгар
    folium.PolyLine(
        locations=[(p[1], p[0]) for p in coords_talgar], 
        color='blue', weight=4, opacity=0.8, tooltip='Река Талгар'
    ).add_to(m)

    # Добавляем русло реки Шынжалы
    folium.PolyLine(
        locations=[(p[1], p[0]) for p in coords_shynzhaly], 
        color='green', weight=4, opacity=0.8, tooltip='Река Шынжалы'
    ).add_to(m)

    # Добавляем маркер пересечения, если оно найдено
    if intersection_point:
        folium.Marker(
            location=intersection_point,
            popup="Точка пересечения рек",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

    # Сохранение карты
    m.save("169.html")
    print("Карта успешно сохранена в файл 169.html")

if __name__ == "__main__":
    solve_river_intersection()