import folium
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Шаг 1: Сбор данных
# Предположим, что у нас есть данные о реках и точках наблюдения за уровнем воды.
# Для примера создадим фейковые данные.

# Координаты рек
bayankol_coords = [(86.9250, 43.1150), (87.0250, 43.2150)]
ili_coords = [(87.6250, 44.9150), (87.7250, 45.0150)]

# Создание GeoDataFrame для рек
bayankol_line = gpd.GeoSeries([LineString(bayankol_coords)])
ili_line = gpd.GeoSeries([LineString(ili_coords)])

bayankol_gdf = gpd.GeoDataFrame({'name': ['Bayankol River'], 'geometry': bayankol_line})
ili_gdf = gpd.GeoDataFrame({'name': ['Ili River'], 'geometry': ili_line})

# Предположим, что у нас есть данные о уровнях воды в точках наблюдения
water_level_data = {
    'river': ['Bayankol River', 'Bayankol River', 'Ili River', 'Ili River'],
    'latitude': [43.1500, 43.2000, 44.9500, 45.0000],
    'longitude': [86.9750, 87.0750, 87.6750, 87.7750],
    'water_level': [120, 130, 140, 150],  # Уровень воды в метрах
    'flood_risk': ['low', 'high', 'medium', 'high']  # Предположительный риск паводка
}

water_level_gdf = gpd.GeoDataFrame(water_level_data, geometry=gpd.points_from_xy(water_level_data['longitude'], water_level_data['latitude']))

# Шаг 2: Подготовка данных
# В данном случае данные уже подготовлены и готовы к использованию.

# Шаг 3: Моделирование риска паводков
# Для простоты предположим, что риск паводка определяется уровнем воды.
# На практике здесь могла бы быть более сложная модель с учетом дополнительных факторов.

# Шаг 4: Визуализация результатов
m = folium.Map(location=[43.5, 87.2], zoom_start=9)

# Добавление рек на карту
folium.GeoJson(bayankol_gdf).add_to(m)
folium.GeoJson(ili_gdf).add_to(m)

# Функция для определения цвета маркера в зависимости от риска паводка
def get_marker_color(risk):
    if risk == 'low':
        return 'green'
    elif risk == 'medium':
        return 'orange'
    else:
        return 'red'

# Добавление точек наблюдения на карту с маркерами, отражающими риск паводка
for _, row in water_level_gdf.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"River: {row['river']}, Water Level: {row['water_level']}m, Flood Risk: {row['flood_risk']}",
        icon=folium.Icon(color=get_marker_color(row['flood_risk']))
    ).add_to(m)

# Сохранение карты в файл
m.save("151.html")