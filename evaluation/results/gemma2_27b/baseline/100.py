import geopandas as gpd
from shapely.geometry import LineString
from shapely.ops import transform
import pyproj

# Загрузка данных о реках
rivers = gpd.read_file("rivers.geojson")

# Фильтрация данных по рекам Шыжын и Дос
start_river = rivers[rivers["name"] == "Шыжын"].iloc[0].geometry
end_river = rivers[rivers["name"] == "Дос"].iloc[0].geometry

# Расчет длины пути
total_length = 0
current_point = start_river

while current_point != end_river:
    # Найти ближайшую реку к текущей точке
    next_river = rivers.loc[rivers["name"] != "Шыжын"].iloc[0].geometry

    # Создать линию между текущей точкой и следующей рекой
    line = LineString([current_point, next_river])

    # Рассчитать длину линии
    length = line.length

    # Суммировать длину отрезка с общей длиной пути
    total_length += length

    # Обновить текущую точку на следующую реку
    current_point = next_river

# Вывод результата
print(f"Общая длина речного пути: {total_length} единиц")

# Визуализация (необязательно)
import folium

# Создать карту
m = folium.Map()

# Добавить реки на карту
folium.GeoJson("rivers.geojson").add_to(m)

# Сохранить карту
m.save("100.html")