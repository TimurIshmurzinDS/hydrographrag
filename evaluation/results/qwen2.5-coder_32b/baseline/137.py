import geopandas as gpd
from shapely.geometry import Point
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть два файла GeoJSON: один с границами рек Или и Каратал, другой с данными о датчиках.
rivers_gdf = gpd.read_file('rivers.geojson')  # Файл должен содержать поля 'name' для названия реки
sensors_gdf = gpd.read_file('sensors.geojson')  # Файл должен содержать поля 'status' (0 - неисправен, 1 - исправен) и координаты

# Шаг 2: Подготовка данных
# Убедимся, что данные в правильной системе координат
rivers_gdf = rivers_gdf.to_crs(epsg=4326)
sensors_gdf = sensors_gdf.to_crs(epsg=4326)

# Шаг 3: Фильтрация датчиков
# Создадим функцию для проверки, находится ли точка внутри полигонов рек
def is_within_river(sensor_point, rivers):
    for _, river in rivers.iterrows():
        if sensor_point.within(river['geometry']):
            return True
    return False

# Применим фильтрацию к датчикам
sensors_gdf['within_rivers'] = sensors_gdf.apply(lambda row: is_within_river(row['geometry'], rivers_gdf), axis=1)
filtered_sensors_gdf = sensors_gdf[sensors_gdf['within_rivers']]

# Шаг 4: Анализ статуса датчиков
malfunctioning_sensors = filtered_sensors_gdf[filtered_sensors_gdf['status'] == 0]
print(f"Количество неисправных датчиков в бассейнах рек Или и Каратал: {len(malfunctioning_sensors)}")

# Шаг 5: Визуализация результатов
# Создадим карту с помощью folium
m = folium.Map(location=[42.8746, 74.5910], zoom_start=10)  # Координаты Бишкека

# Добавим границы рек на карту
folium.GeoJson(rivers_gdf).add_to(m)

# Добавим датчики на карту
for _, sensor in filtered_sensors_gdf.iterrows():
    point = sensor['geometry']
    folium.CircleMarker(
        location=[point.y, point.x],
        radius=5,
        color='green' if sensor['status'] == 1 else 'red',
        fill=True,
        fill_color='green' if sensor['status'] == 1 else 'red'
    ).add_to(m)

# Сохранение карты
m.save("137.html")