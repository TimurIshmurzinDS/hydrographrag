import geopandas as gpd
from shapely.geometry import Point, LineString
import folium

# Шаг 1: Сбор данных (в данном примере предположим, что у нас есть GeoDataFrame с руслами рек)
# Для демонстрации создадим искусственные данные
data = {
    'name': ['Емель', 'Тентек', 'Быж'],
    'geometry': [
        LineString([(30.5, 60), (31, 60.5), (32, 61)]),
        LineString([(30, 60.2), (30.4, 60.3)]),
        LineString([(31.8, 60.7), (32, 60.9)])
    ]
}

# Создание GeoDataFrame
gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

# Шаг 2: Анализ геометрии
emel_line = gdf[gdf['name'] == 'Емель'].iloc[0].geometry

def is_tributary(tributary_line, main_line):
    # Проверка пересечения линий или наличия начала притока внутри водосборной области основной реки
    return tributary_line.intersects(main_line) or main_line.contains(tributary_line.boundary[0])

# Определение притоков
results = {}
for index, row in gdf[gdf['name'] != 'Емель'].iterrows():
    results[row['name']] = is_tributary(row.geometry, emel_line)

print("Результаты анализа:")
for river, is_trib in results.items():
    print(f"Река {river} является притоком реки Емель: {'Да' if is_trib else 'Нет'}")

# Шаг 3: Визуализация результатов
m = folium.Map(location=[60.5, 31], zoom_start=8)

# Добавление линий на карту
for index, row in gdf.iterrows():
    points = [(p.y, p.x) for p in row.geometry.coords]
    color = 'blue' if row['name'] == 'Емель' else ('green' if results.get(row['name'], False) else 'red')
    folium.PolyLine(points, color=color, weight=2.5, opacity=1).add_to(m)

# Сохранение карты
m.save("101.html")