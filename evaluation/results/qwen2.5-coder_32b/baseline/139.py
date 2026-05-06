import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть два файла:
# - rivers.geojson: геоданные о реках в формате GeoJSON
# - water_level_data.csv: данные с датчиков уровня воды (столбцы: sensor_id, latitude, longitude, water_level)

rivers = gpd.read_file('rivers.geojson')
water_level_data = pd.read_csv('water_level_data.csv')

# Шаг 2: Предварительная обработка данных
# Преобразуем данные с датчиков в GeoDataFrame
geometry = [Point(xy) for xy in zip(water_level_data['longitude'], water_level_data['latitude'])]
gdf_water_level = gpd.GeoDataFrame(water_level_data, geometry=geometry)

# Шаг 3: Определение нормальных значений уровня воды
# Предположим, что мы уже знаем диапазон нормальных значений (например, от 0 до 5 метров)
normal_range = (0, 5)

# Шаг 4: Выявление аномалий
anomalies = gdf_water_level[(gdf_water_level['water_level'] < normal_range[0]) | 
                            (gdf_water_level['water_level'] > normal_range[1])]

# Шаг 5: Геоспатиальное моделирование
# Определяем, какие из аномалий находятся в пределах реки Сарыкан
sarykan_river = rivers[rivers['name'] == 'Сарыкан']
anomalies_in_sarykan = gpd.sjoin(anomalies, sarykan_river, how="inner", op='within')

# Шаг 6: Визуализация результатов
# Создаем интерактивную карту с помощью folium
m = folium.Map(location=[sarykan_river.centroid.y.mean(), sarykan_river.centroid.x.mean()], zoom_start=10)

# Добавляем реки на карту
folium.GeoJson(sarykan_river).add_to(m)

# Добавляем аномалии на карту
for _, row in anomalies_in_sarykan.iterrows():
    folium.Marker(
        location=[row['geometry'].y, row['geometry'].x],
        popup=f"Аномальный уровень воды: {row['water_level']} м",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохраняем карту в файл
m.save("139.html")