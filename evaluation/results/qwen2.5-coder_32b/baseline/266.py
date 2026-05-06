import folium
from shapely.geometry import Polygon, Point
import geopandas as gpd
import random

# Шаг 1: Сбор данных (примерные координаты полей)
fields = [
    Polygon([(50.2, 46.3), (50.4, 46.3), (50.4, 46.5), (50.2, 46.5)]),
    Polygon([(50.1, 46.4), (50.3, 46.4), (50.3, 46.6), (50.1, 46.6)])
]

# Создание GeoDataFrame
gdf_fields = gpd.GeoDataFrame(geometry=fields)

# Шаг 2: Анализ данных (простой пример - случайное определение зон поливных нужд)
gdf_fields['irrigation_need'] = [random.choice(['low', 'medium', 'high']) for _ in range(len(gdf_fields))]

# Шаг 3: Моделирование полива
def irrigation_schedule(irrigation_need):
    if irrigation_need == 'low':
        return "1 раз в неделю, 20 минут"
    elif irrigation_need == 'medium':
        return "2 раза в неделю, 40 минут"
    else:
        return "3 раза в неделю, 60 минут"

gdf_fields['schedule'] = gdf_fields['irrigation_need'].apply(irrigation_schedule)

# Шаг 4: Визуализация результатов
m = folium.Map(location=[50.25, 46.45], zoom_start=10)

# Добавление полей на карту
for _, row in gdf_fields.iterrows():
    folium.GeoJson(row['geometry']).add_to(m)
    popup_text = f"Полив: {row['irrigation_need']}\nРасписание: {row['schedule']}"
    folium.Marker(
        location=row['geometry'].centroid.coords[0],
        popup=popup_text
    ).add_to(m)

# Сохранение карты в HTML файл
m.save("266.html")