import geopandas as gpd
from shapely.geometry import LineString
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка данных о реке Караой
river_data = gpd.read_file('karaoy.shp')

# Создание сетки сечений вдоль течения реки
section_size = 1000  # метров
sections = []
for i in range(0, river_data.length.max(), section_size):
    section = LineString([(river_data.geometry.iloc[i].coords[0], river_data.geometry.iloc[i].coords[1]),
                          (river_data.geometry.iloc[i+1].coords[0], river_data.geometry.iloc[i+1].coords[1])])
    sections.append(section)

# Создание точки старта и финиша
start_point = sections[0].coords[0]
end_point = sections[-1].coords[1]

# Определение оптимального пути робота между двумя точками с помощью алгоритма A\*
from heapq import heapify, heappop, heappush

def a_star(start, end):
    open_set = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    while open_set:
        _, current = heappop(open_set)
        if current == end:
            break
        for neighbor in sections:
            new_cost = cost_so_far[current] + neighbor.length
            if neighbor.coords[0] not in came_from and new_cost < cost_so_far.get(neighbor.coords[0], float('inf')):
                cost_so_far[neighbor.coords[0]] = new_cost
                priority = new_cost + neighbor.length
                heappush(open_set, (priority, neighbor.coords[0]))
                came_from[neighbor.coords[0]] = current

    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    return list(reversed(path))

# Создание интерактивной карты с помощью библиотеки Folium
m = folium.Map(location=[42.5, 74.0], zoom_start=10)

# Добавление точки старта и финиша на карту
folium.Marker([start_point[1], start_point[0]], popup='Начало').add_to(m)
folium.Marker([end_point[1], end_point[0]], popup='Конец').add_to(m)

# Добавление оптимального пути робота на карту
path = a_star(start_point, end_point)
for i in range(len(path) - 1):
    folium.PolyLine([(path[i][1], path[i][0]), (path[i+1][1], path[i+1][0])]).add_to(m)

# Сохранение карты в файле HTML
m.save("224.html")