import folium
from shapely.geometry import Point
import geopandas as gpd

# Шаг 1: Сбор данных
# Предположим, что у нас есть данные о притоках реки Каскелен в формате GeoJSON или другом геоданных формате.
# Для примера создадим искусственные данные.

# Координаты притоков (широта, долгота)
confluences = [
    (51.7083, 46.2967),  # Примерные координаты
    (51.7183, 46.3067),
    (51.7283, 46.3167)
]

# Создание GeoDataFrame с использованием geopandas
geometry = [Point(xy) for xy in confluences]
gdf_confluences = gpd.GeoDataFrame(geometry=geometry, crs="EPSG:4326")

# Шаг 2: Анализ данных
# Предположим, что мы хотим выбрать притоки с определенными характеристиками.
# Для простоты выберем все притоки.

# Шаг 3: Моделирование
# В данном случае модель может быть очень простой - выбор всех доступных притоков.
selected_confluences = gdf_confluences

# Шаг 4: Визуализация
# Создание карты с использованием folium
m = folium.Map(location=[51.72, 46.30], zoom_start=13)

# Добавление маркеров на карту для каждого притока
for _, row in selected_confluences.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup="Приток реки Каскелен",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в HTML файл
m.save("247.html")