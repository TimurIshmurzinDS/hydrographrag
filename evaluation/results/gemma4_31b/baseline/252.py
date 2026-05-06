import folium
from shapely.geometry import Point, LineString, Polygon
from shapely.ops import unary_union

def solve_gis_smart_contract():
    # 1. Координаты реки Дос (упрощенный массив точек для моделирования русла)
    # В реальном проекте здесь используется GeoJSON или Shapefile
    dos_river_coords = [
        [52.50, 65.10], [52.55, 65.30], [52.60, 65.50], 
        [52.65, 65.70], [52.70, 65.90], [52.75, 66.10]
    ]
    
    # 2. Создание линейного объекта реки
    river_line = LineString(dos_river_coords)
    
    # 3. Создание буферной зоны (Geofence) 
    # 0.005 градуса примерно равно 500-600 метрам
    buffer_distance = 0.005 
    river_buffer = river_line.buffer(buffer_distance)
    
    # 4. Симуляция координат устройства (например, датчика качества воды или лодки)
    # Точка А: Внутри зоны реки (Контракт должен сработать)
    test_point_inside = Point(52.60, 65.501) 
    # Точка Б: Вне зоны реки (Контракт не должен сработать)
    test_point_outside = Point(52.80, 66.00)
    
    def check_contract_trigger(point, zone):
        """Симуляция работы Оракула: проверка вхождения точки в зону"""
        return zone.contains(point)

    # Проверка условий
    status_inside = check_contract_trigger(test_point_inside, river_buffer)
    status_outside = check_contract_trigger(test_point_outside, river_buffer)
    
    print(f"Trigger for Point Inside: {'ACTIVE' if status_inside else 'INACTIVE'}")
    print(f"Trigger for Point Outside: {'ACTIVE' if status_outside else 'INACTIVE'}")

    # 5. Визуализация с помощью folium
    # Центрируем карту на среднем значении координат
    m = folium.Map(location=[52.6, 65.5], zoom_start=8, tiles='OpenStreetMap')
    
    # Рисуем русло реки
    folium.PolyLine(dos_river_coords, color="blue", weight=4, opacity=0.8, tooltip="Река Дос").add_to(m)
    
    # Рисуем буферную зону (Geofence)
    # Преобразуем shapely Polygon в список координат для folium
    if isinstance(river_buffer, Polygon):
        coords_buffer = list(river_buffer.exterior.coords)
        folium.Polygon(coords_buffer, color="green", fill=True, fill_opacity=0.3, 
                      tooltip="Зона действия смарт-контракта").add_to(m)
    
    # Добавляем тестовые точки
    folium.Marker(
        location=[test_point_inside.y, test_point_inside.x], 
        popup="Точка А: Контракт АКТИВИРОВАН", 
        icon=folium.Icon(color='green', icon='check')
    ).add_to(m)
    
    folium.Marker(
        location=[test_point_outside.y, test_point_outside.x], 
        popup="Точка Б: Контракт НЕ АКТИВИРОВАН", 
        icon=folium.Icon(color='red', icon='times')
    ).add_to(m)
    
    # Сохранение карты
    m.save("252.html")
    print("Map has been saved as 252.html")

if __name__ == "__main__":
    solve_gis_smart_contract()