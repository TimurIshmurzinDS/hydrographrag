import geopandas as gpd
from shapely.geometry import LineString, Point
import folium

# Загрузка геоданных о водных системах (примерный путь к файлу)
water_network = gpd.read_file('path_to_water_network.shp')

# Фильтрация данных для получения только рек
rivers = water_network[water_network['type'] == 'river']

# Определение точек начала и конца маршрута
start_point = Point(86.9250, 43.1750)  # Примерные координаты Шыжын
end_point = Point(87.2500, 43.3000)    # Примерные координаты Дос

# Функция для поиска ближайшего участка реки к точке
def find_nearest_river_segment(point, rivers):
    nearest = min(rivers.geometry, key=lambda geom: point.distance(geom))
    return nearest

# Поиск ближайших участков реки к начальной и конечной точкам
start_segment = find_nearest_river_segment(start_point, rivers)
end_segment = find_nearest_river_segment(end_point, rivers)

# Функция для поиска маршрута между двумя участками реки
def find_route(start_segment, end_segment, rivers):
    # Простая реализация алгоритма поиска пути (не оптимальная)
    visited = set()
    queue = [(start_segment, [start_segment])]
    
    while queue:
        current_segment, path = queue.pop(0)
        
        if current_segment == end_segment:
            return path
        
        visited.add(current_segment)
        
        # Поиск соседних участков
        neighbors = rivers[rivers.touches(current_segment)]
        for neighbor in neighbors.geometry:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    
    return None

# Поиск маршрута
route_segments = find_route(start_segment, end_segment, rivers)

if route_segments is not None:
    # Расчет общей длины маршрута
    total_length = sum(segment.length for segment in route_segments)
    print(f"Общая длина речного пути: {total_length} метров")
    
    # Создание карты с использованием folium
    m = folium.Map(location=[43.25, 87.1], zoom_start=10)
    
    # Добавление маршрута на карту
    for segment in route_segments:
        folium.PolyLine(locations=list(segment.coords), color='blue', weight=2.5).add_to(m)
    
    # Добавление начальной и конечной точек на карту
    folium.Marker([start_point.y, start_point.x], popup="Шыжын", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker([end_point.y, end_point.x], popup="Дос", icon=folium.Icon(color='red')).add_to(m)
    
    # Сохранение карты в файл
    m.save("100.html")
else:
    print("Маршрут не найден.")