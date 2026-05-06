import folium
from math import radians, sin, cos, sqrt, atan2

# Координаты созвездия Ориона (предположим)
oriion_coords = [28.0, 48.0]

# Координаты реки Шилик (предположим)
shilik_coords = [25.5, 45.0]

# Функция для расчета расстояния между двумя точками
def distance(lat1, lon1, lat2, lon2):
    R = 6371  # радиус Земли в километрах
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) * sin(dlat / 2) + cos(radians(lat1)) \
        * cos(radians(lat2)) * sin(dlon / 2) * sin(dlon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Функция для поиска кратчайшего пути
def shortest_path(start, end):
    # Используем алгоритм Dijkstra для нахождения кратчайшего пути
    graph = {}
    for lat in range(-90, 91):
        for lon in range(-180, 181):
            graph[(lat, lon)] = {}
            for dlat in [-1, 0, 1]:
                for dlon in [-1, 0, 1]:
                    if (dlat == 0 and dlon == 0) or abs(dlat) + abs(dlon) > 1:
                        continue
                    lat2 = lat + dlat
                    lon2 = lon + dlon
                    graph[(lat, lon)][(lat2, lon2)] = distance(lat, lon, lat2, lon2)
    queue = [(start, 0)]
    visited = set()
    while queue:
        (node, dist) = queue.pop(0)
        if node == end:
            return dist
        if node in visited:
            continue
        visited.add(node)
        for neighbor, weight in graph[node].items():
            queue.append((neighbor, dist + weight))
    return -1  # если кратчайшего пути не существует

# Поиск кратчайшего пути между созвездием Ориона и рекой Шилик
path_length = shortest_path(oriion_coords, shilik_coords)

# Визуализация результата на карте
m = folium.Map(location=[oriion_coords[0], oriion_coords[1]], zoom_start=4)
folium.Marker([oriion_coords[0], oriion_coords[1]], popup='Созвездие Ориона').add_to(m)
folium.Marker([shilik_coords[0], shilik_coords[1]], popup='Река Шилик').add_to(m)
m.save("246.html")
print(f"Длина кратчайшего пути: {path_length} км")