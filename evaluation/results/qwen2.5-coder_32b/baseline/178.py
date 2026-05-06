import geopandas as gpd
from shapely.geometry import LineString, Point
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть GeoDataFrame с речными сетями региона
# Для примера создадим небольшой набор данных
data = {
    'name': ['Тентек', 'Приток1', 'Приток2', 'Приток3'],
    'geometry': [
        LineString([(0, 0), (5, 5)]),
        LineString([(2, 2), (4, 4)]),
        LineString([(1, 1), (3, 3)]),
        LineString([(6, 6), (7, 7)])
    ]
}

# Создание GeoDataFrame
rivers_gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

# Шаг 2: Подготовка данных
# Добавление атрибутов для анализа топологии
def calculate_order(geom):
    # Простой пример вычисления порядкового номера притока (в реальности может быть более сложным)
    return len(list(geom.coords))

rivers_gdf['order'] = rivers_gdf['geometry'].apply(calculate_order)

# Шаг 3: Анализ топологии
# Пример анализа: вычисление среднего порядкового номера притоков
average_order = rivers_gdf[rivers_gdf['name'] != 'Тентек']['order'].mean()
print(f"Средний порядковый номер притоков реки Тентек: {average_order}")

# Шаг 4: Визуализация результатов
# Создание карты с использованием folium
m = folium.Map(location=[3, 3], zoom_start=5)

# Добавление речных сетей на карту
for _, row in rivers_gdf.iterrows():
    coords = [(p.y, p.x) for p in row['geometry'].coords]
    folium.PolyLine(coords, color='blue', weight=2.5, opacity=1).add_to(m)
    
# Добавление маркеров с информацией о порядке притоков
for _, row in rivers_gdf.iterrows():
    if row['name'] != 'Тентек':
        coords = [(p.y, p.x) for p in row['geometry'].coords][0]
        folium.Marker(coords, popup=f"Приток: {row['name']}, Порядок: {row['order']}").add_to(m)

# Шаг 5: Сохранение карты
m.save("178.html")