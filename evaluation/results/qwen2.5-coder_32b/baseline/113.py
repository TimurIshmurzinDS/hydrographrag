import folium
import geopandas as gpd
from shapely.geometry import Point, Polygon

# Шаг 1: Сбор данных (примерные данные)
# Предположим, у нас есть геоданные о реках и их текущих уровнях воды
data = {
    'river': ['Lepsy River', 'Sarykan River'],
    'latitude': [50.2345, 49.8765],
    'longitude': [123.4567, 122.8765],
    'current_water_level': [1.5, 2.0],  # в метрах
    'predicted_water_level': [1.0, 1.5]   # предполагаемый уровень воды после снижения
}

# Создание GeoDataFrame
gdf = gpd.GeoDataFrame(data, geometry=[Point(xy) for xy in zip(data['longitude'], data['latitude'])])

# Шаг 2: Анализ текущего состояния (простой пример)
# Предположим, что мы уже знаем текущие уровни воды и хотим визуализировать их

# Шаг 3: Моделирование сценариев снижения уровня воды
# Здесь можно использовать более сложные модели гидрологии, но для примера просто используем предполагаемые значения

# Шаг 4: Оценка экологических последствий
# Предположим, что снижение уровня воды приводит к изменению типов растительного покрова и распределения животных
# Для простоты создадим два полигона для каждого реки с разными цветами

polygons = []
for idx, row in gdf.iterrows():
    # Создаем полигон вокруг точки (река) радиусом 0.1 градусов
    polygon = Polygon([
        (row['longitude'] - 0.1, row['latitude'] - 0.1),
        (row['longitude'] + 0.1, row['latitude'] - 0.1),
        (row['longitude'] + 0.1, row['latitude'] + 0.1),
        (row['longitude'] - 0.1, row['latitude'] + 0.1)
    ])
    polygons.append(polygon)

gdf['geometry'] = polygons

# Шаг 5: Визуализация результатов
m = folium.Map(location=[49.8765, 123.4567], zoom_start=9)

for idx, row in gdf.iterrows():
    # Добавляем полигон на карту с цветом в зависимости от уровня воды
    color = 'green' if row['predicted_water_level'] > 1.0 else 'red'
    folium.GeoJson(row['geometry'], style_function=lambda x: {'fillColor': color, 'color': color}).add_to(m)
    
    # Добавляем маркер с информацией о реке
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Река: {row['river']}\nТекущий уровень воды: {row['current_water_level']} м\nПредполагаемый уровень воды: {row['predicted_water_level']} м",
        icon=folium.Icon(color=color)
    ).add_to(m)

# Сохранение карты
m.save("113.html")