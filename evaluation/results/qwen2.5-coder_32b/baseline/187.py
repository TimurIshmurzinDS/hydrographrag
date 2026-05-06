import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть геоданные о животноводческих хозяйствах и реке Токыраун.
# Для примера создадим эти данные искусственно.

# Координаты животноводческих хозяйств (longitude, latitude)
farms_coords = [
    (76.950833, 42.861667),
    (77.000000, 42.850000),
    (76.983333, 42.833333)
]

# Создание GeoDataFrame для животноводческих хозяйств
farms = gpd.GeoDataFrame(
    {'name': ['Хозяйство1', 'Хозяйство2', 'Хозяйство3'],
     'geometry': [Point(xy) for xy in farms_coords]},
    crs="EPSG:4326"
)

# Координаты реки Токыраун (простая линия для примера)
river_coords = [
    (76.900000, 42.850000),
    (77.100000, 42.850000)
]

# Создание GeoDataFrame для реки
river = gpd.GeoDataFrame(
    {'name': ['Река Токыраун'],
     'geometry': [Polygon([Point(xy) for xy in river_coords])]},
    crs="EPSG:4326"
)

# Шаг 2: Определение зон влияния
# Предположим, что радиус влияния реки составляет 1 км.
buffer_distance = 1000  # в метрах

# Создание буфера вокруг реки
river_buffer = river.buffer(buffer_distance)

# Шаг 3: Моделирование потребления воды
# Предположим, что каждое животное потребляет 50 литров воды в день.
water_consumption_per_animal = 50  # в литрах

# Данные о количестве животных на каждом хозяйстве
farms['animal_count'] = [100, 200, 150]  # количество животных на каждом хозяйстве

# Расчет ежедневного потребления воды каждым хозяйством
farms['daily_water_consumption'] = farms['animal_count'] * water_consumption_per_animal

# Шаг 4: Анализ влияния
# Определение хозяйств, находящихся в зоне влияния реки
affected_farms = gpd.sjoin(farms, river_buffer, how="inner", op='within')

# Расчет общего потребления воды затронутыми хозяйствами
total_water_consumption_affected = affected_farms['daily_water_consumption'].sum()

print(f"Общее ежедневное потребление воды затронутыми хозяйствами: {total_water_consumption_affected} литров")

# Шаг 5: Визуализация результатов
m = folium.Map(location=[42.850000, 76.950833], zoom_start=12)

# Добавление реки на карту
folium.GeoJson(river_buffer).add_to(m)

# Добавление хозяйств на карту с цветовой маркировкой в зависимости от их влияния
for _, farm in farms.iterrows():
    if farm['name'] in affected_farms['name'].values:
        color = 'red'  # затронутые хозяйства
    else:
        color = 'blue'  # незатронутые хозяйства
    
    folium.Marker(
        location=[farm.geometry.y, farm.geometry.x],
        popup=f"Хозяйство: {farm['name']}, Потребление воды: {farm['daily_water_consumption']} литров/день",
        icon=folium.Icon(color=color)
    ).add_to(m)

# Сохранение карты
m.save("187.html")