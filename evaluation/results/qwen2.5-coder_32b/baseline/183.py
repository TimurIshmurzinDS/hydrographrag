import folium
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Шаг 1: Сбор данных
# Предположим, что у нас есть данные о реке и садах в формате GeoJSON или CSV.
# Для примера создадим искусственные данные.

# Данные о реке Турген (уровень воды и скорость течения)
river_data = {
    'name': ['Турген'],
    'level': [1.5],  # Уровень воды в метрах
    'velocity': [2.0]  # Скорость течения в м/с
}

# Данные о садах (координаты и потребность в воде)
gardens_data = {
    'name': ['Сад1', 'Сад2', 'Сад3'],
    'latitude': [42.87, 42.90, 42.85],
    'longitude': [74.60, 74.65, 74.55],
    'water_need': [1000, 1500, 1200]  # Потребность в воде в литрах
}

# Шаг 2: Обработка данных
river_df = pd.DataFrame(river_data)
gardens_df = pd.DataFrame(gardens_data)

# Преобразуем данные садов в GeoDataFrame
geometry = [Point(xy) for xy in zip(gardens_df['longitude'], gardens_df['latitude'])]
gardens_gdf = gpd.GeoDataFrame(gardens_df, geometry=geometry)

# Шаг 3: Моделирование
# Простая модель: если уровень воды выше определенного порога (например, 1.0 м), то сады могут быть орошены.
water_threshold = 1.0

gardens_gdf['is_irrigable'] = gardens_gdf.apply(lambda row: 'Да' if river_df['level'].values[0] > water_threshold else 'Нет', axis=1)

# Шаг 4: Анализ
print(gardens_gdf[['name', 'water_need', 'is_irrigable']])

# Шаг 5: Визуализация
m = folium.Map(location=[42.87, 74.60], zoom_start=13)

# Добавление садов на карту
for _, garden in gardens_gdf.iterrows():
    color = 'green' if garden['is_irrigable'] == 'Да' else 'red'
    folium.Marker(
        location=[garden['latitude'], garden['longitude']],
        popup=f"Сад: {garden['name']}<br>Потребность в воде: {garden['water_need']} л<br>Орошение возможно: {garden['is_irrigable']}",
        icon=folium.Icon(color=color)
    ).add_to(m)

# Добавление реки на карту (для простоты - точка)
folium.Marker(
    location=[42.87, 74.60],
    popup=f"Река Турген<br>Уровень воды: {river_df['level'].values[0]} м",
    icon=folium.Icon(color='blue')
).add_to(m)

# Сохранение карты
m.save("183.html")