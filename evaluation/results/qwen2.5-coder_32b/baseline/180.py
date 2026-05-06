import geopandas as gpd
from shapely.geometry import Point, LineString
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть GeoDataFrame с речными сетями региона
# Для примера создадим небольшой набор данных
data = {
    'name': ['Текес', 'Сарыкан', 'Река1', 'Река2'],
    'geometry': [
        LineString([(80.3, 42.5), (80.6, 42.7), (80.9, 42.9)]),
        LineString([(80.4, 42.6), (80.7, 42.8), (81.0, 43.0)]),
        LineString([(80.5, 42.7), (80.8, 42.9), (81.1, 43.1)]),
        LineString([(80.6, 42.8), (80.9, 43.0), (81.2, 43.2)])
    ]
}

# Создание GeoDataFrame
rivers_gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

# Шаг 2: Подготовка данных
# В данном примере предположим, что данные уже очищены

# Шаг 3: Идентификация речных сетей
tekkes = rivers_gdf[rivers_gdf['name'] == 'Текес']
sarykan = rivers_gdf[rivers_gdf['name'] == 'Сарыкан']

# Шаг 4: Анализ конфигурации
# Для простоты предположим, что мы ищем точку сливания двух рек
intersection_point = None

for geom1 in tekkes.geometry:
    for geom2 in sarykan.geometry:
        if geom1.intersects(geom2):
            intersection_point = geom1.intersection(geom2)
            break
    if intersection_point:
        break

# Шаг 5: Визуализация результатов
# Создание карты с использованием folium
m = folium.Map(location=[42.7, 80.6], zoom_start=9)

# Добавление рек на карту
folium.GeoJson(tekkes).add_to(m)
folium.GeoJson(sarykan).add_to(m)

# Если найдена точка сливания, добавляем её на карту
if intersection_point:
    folium.Marker(
        location=[intersection_point.y, intersection_point.x],
        popup='Точка сливания Текес и Сарыкан',
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("180.html")