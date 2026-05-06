import geopandas as gpd
from shapely.geometry import Point, LineString
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть GeoDataFrame для рек Емель и Каратал.
# Для примера создадим эти данные искусственно.

# Координаты точек реки Емель (примерные)
emel_coords = [
    (86.904297, 43.155000),
    (86.904300, 43.155100),
    (86.904400, 43.155200),
    (86.904500, 43.155300),
    (86.904600, 43.155400)
]

# Координаты точек реки Каратал (примерные)
karatal_coords = [
    (86.904700, 43.155500),
    (86.904800, 43.155600),
    (86.904900, 43.155700),
    (86.904600, 43.155400)  # Точка слияния с рекой Емель
]

# Создание GeoDataFrame для реки Емель
emel_line = LineString(emel_coords)
emel_gdf = gpd.GeoDataFrame({'name': ['Емель'], 'geometry': [emel_line]})

# Создание GeoDataFrame для реки Каратал
karatal_line = LineString(karatal_coords)
karatal_gdf = gpd.GeoDataFrame({'name': ['Каратал'], 'geometry': [karatal_line]})

# Шаг 2: Анализ топологии
# Проверка пересечения рек и определение точки слияния
intersection_point = emel_line.intersection(karatal_line)

if intersection_point.is_empty:
    print("Река Емель не является притоком реки Каратал.")
else:
    # Шаг 3: Вычисление длины участка
    # Определяем точку пересечения и вычисляем длину участка реки Емель до точки слияния
    emel_to_intersection = LineString([emel_coords[0], intersection_point])
    length_emel_to_intersection = emel_to_intersection.length
    
    print(f"Река Емель является притоком реки Каратал. Длина участка: {length_emel_to_intersection} градусов.")
    
    # Шаг 4: Визуализация результатов
    m = folium.Map(location=[43.155000, 86.904297], zoom_start=15)
    
    # Добавление реки Емель на карту
    folium.PolyLine(emel_coords, color="blue", weight=2.5, opacity=1).add_to(m)
    
    # Добавление реки Каратал на карту
    folium.PolyLine(karatal_coords, color="green", weight=2.5, opacity=1).add_to(m)
    
    # Добавление точки слияния на карту
    folium.Marker(
        location=[intersection_point.y, intersection_point.x],
        popup='Точка слияния рек Емель и Каратал',
        icon=folium.Icon(color="red")
    ).add_to(m)
    
    m.save("97.html")