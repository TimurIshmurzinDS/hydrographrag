import geopandas as gpd
import numpy as np
from shapely.geometry import Point, LineString
import folium

# 1. Загрузить данные о топографической сети притоков реки Тентек в формате вектора.
tentek_network = gpd.read_file("tentek_network.shp")

# 2. Создать точку старта для спутниковой орбиты и определить направление движения спутника.
start_point = Point(85.0, 41.0)
direction = np.pi / 2  # Направление на восток

# 3. Рассчитать траекторию полета спутника, учитывая его скорость и время полета.
satellite_speed = 7680  # Скорость спутника в км/ч
flight_time = 120  # Время полета в минутах

distance_flown = satellite_speed * flight_time / 60  # Расстояние, пролететое спутником за время полета в км
trajectory = LineString([start_point] + [Point(start_point.x + distance * np.cos(direction),
                                                start_point.y + distance * np.sin(direction))
                                         for distance in np.arange(0, distance_flown, 1)])

# 4. Проанализировать пересечение траектории полета со сетью притоков реки Тентек.
intersections = gpd.sjoin(tentek_network, trajectory, how="intersection", predicate="intersects")

# 5. Визуализировать результаты на карте с использованием библиотеки `folium`.
m = folium.Map(location=[start_point.y, start_point.x], zoom_start=8)

# Добавить траекторию полета спутника на карту.
folium.GeoJson(trajectory, style_function=lambda x: {'fillColor': 'blue', 'color': 'blue'}).add_to(m)

# Добавить сеть притоков реки Тентек на карту.
tentek_network_geojson = tentek_network.to_json()
folium.GeoJson(tentek_network_geojson, style_function=lambda x: {'fillColor': '#3db7e4', 'color': '#3db7e4'}).add_to(m)

# Добавить точки пересечения траектории полета со сетью притоков реки Тентек на карту.
for _, row in intersections.iterrows():
    folium.CircleMarker(location=[row.geometry.y, row.geometry.x], radius=5, color='red').add_to(m)

# Сохранить карту в формате HTML.
m.save("250.html")