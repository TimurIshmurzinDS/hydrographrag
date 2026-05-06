import geopandas as gpd
from shapely.geometry import LineString, Point
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть GeoDataFrame с руслами рек и их притоков.
# Для примера создадим эти данные вручную.

# Координаты точек для реки Улькен Алматы
ulkun_almaty_coords = [
    (76.9345, 42.8105), (76.9350, 42.8110), (76.9355, 42.8115),
    (76.9360, 42.8120), (76.9365, 42.8125)
]

# Координаты точек для реки Шыжын
shyzyn_coords = [
    (76.9370, 42.8130), (76.9375, 42.8135), (76.9380, 42.8140),
    (76.9385, 42.8145), (76.9390, 42.8150)
]

# Координаты точек для притока реки Улькен Алматы
pritok_ulkun_almaty_coords = [
    (76.9340, 42.8100), (76.9345, 42.8105), (76.9350, 42.8110)
]

# Создание GeoDataFrame
ulkun_almaty = gpd.GeoSeries([LineString(ulkun_almaty_coords)], crs="EPSG:4326")
shyzyn = gpd.GeoSeries([LineString(shyzyn_coords)], crs="EPSG:4326")
pritok_ulkun_almaty = gpd.GeoSeries([LineString(pritok_ulkun_almaty_coords)], crs="EPSG:4326")

# Шаг 2: Подготовка данных
# Создание DataFrame с названиями рек и их геометриями
rivers = gpd.GeoDataFrame({
    'name': ['Улькен Алматы', 'Шыжын', 'Приток Улькен Алматы'],
    'geometry': [ulkun_almaty[0], shyzyn[0], pritok_ulkun_almaty[0]]
})

# Шаг 3: Анализ гидрографической сети
# Проверка пересечений между руслами рек и их притоков
intersections = []
for i in range(len(rivers)):
    for j in range(i + 1, len(rivers)):
        if rivers.iloc[i].geometry.intersects(rivers.iloc[j].geometry):
            intersections.append((rivers.iloc[i]['name'], rivers.iloc[j]['name']))

# Вывод результатов
if intersections:
    print("Реки и их притоки пересекаются:")
    for intersection in intersections:
        print(f"{intersection[0]} и {intersection[1]}")
else:
    print("Реки Улькен Алматы и Шыжын не связаны через систему притоков.")

# Шаг 4: Визуализация результатов
# Создание карты с использованием folium
m = folium.Map(location=[42.8130, 76.9350], zoom_start=14)

# Добавление русел рек и их притоков на карту
for _, row in rivers.iterrows():
    points = [(lat, lon) for lon, lat in list(row['geometry'].coords)]
    folium.PolyLine(points, color='blue', weight=2.5, opacity=1).add_to(m)

# Сохранение карты в файл
m.save("95.html")