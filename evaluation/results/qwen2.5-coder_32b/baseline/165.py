import folium
import geopandas as gpd
from shapely.geometry import Point, LineString
import pandas as pd

# Шаг 1: Сбор данных
# Предположим, что у нас есть географические данные о реках в формате GeoJSON.
shyzhyn_river = gpd.read_file('shyzhyn_river.geojson')
sarykan_river = gpd.read_file('sarykan_river.geojson')

# Предположим, что у нас есть исторические данные о выпадении осадков и уровнях воды.
precipitation_data = pd.read_csv('precipitation_data.csv')  # Данные о осадках
water_level_data = pd.read_csv('water_level_data.csv')      # Данные об уровне воды

# Шаг 2: Подготовка данных
# Очистка и предварительная обработка данных.
shyzhyn_river_cleaned = shyzhyn_river.dropna()
sarykan_river_cleaned = sarykan_river.dropna()

precipitation_data_cleaned = precipitation_data.dropna()
water_level_data_cleaned = water_level_data.dropna()

# Шаг 3: Создание модели гидрологического процесса
# Для простоты предположим, что мы используем простую модель для определения риска паводков.
# Например, если уровень воды превышает определенный порог, считаем это паводком.

def is_flood(water_level):
    flood_threshold = 10.0  # Примерный порог уровня воды для паводка
    return water_level > flood_threshold

water_level_data_cleaned['is_flood'] = water_level_data_cleaned['water_level'].apply(is_flood)

# Шаг 4: Анализ риска паводков
# Определяем участки рек, где произошли паводки.
flood_events = water_level_data_cleaned[water_level_data_cleaned['is_flood']]

# Шаг 5: Визуализация результатов
# Создаем интерактивную карту с помощью folium.
m = folium.Map(location=[42.8746, 74.5910], zoom_start=10)  # Координаты примерного центра региона

# Добавляем реки на карту
folium.GeoJson(shyzhyn_river_cleaned).add_to(m)
folium.GeoJson(sarykan_river_cleaned).add_to(m)

# Добавляем точки паводковых событий
for _, row in flood_events.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Паводок: Уровень воды {row['water_level']}",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохраняем карту в файл
m.save("165.html")