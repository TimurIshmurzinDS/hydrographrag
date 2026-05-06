import geopandas as gpd
from shapely.geometry import Point, LineString
import folium

# Шаг 1: Загрузка данных
# Предположим, что у нас есть два файла GeoJSON: 'emel_catchment.geojson' и 'sarykan_river.geojson'
emel_catchment = gpd.read_file('emel_catchment.geojson')
sarykan_river = gpd.read_file('sarykan_river.geojson')

# Шаг 2: Анализ топологической связности
# Проверка, пересекается ли река Сарыкан с бассейном реки Эмель
intersection = sarykan_river.intersects(emel_catchment.unary_union)

if intersection.any():
    print("Река Сарыкан имеет топологическую связность с бассейном реки Эмель.")
else:
    print("Река Сарыкан не имеет топологической связи с бассейном реки Эмель.")

# Шаг 3: Визуализация результатов
# Создание карты
m = folium.Map(location=[emel_catchment.centroid.y.mean(), emel_catchment.centroid.x.mean()], zoom_start=10)

# Добавление бассейна реки Эмель на карту
folium.GeoJson(emel_catchment, name='Бассейн реки Эмель').add_to(m)

# Добавление реки Сарыкан на карту
folium.GeoJson(sarykan_river, name='Река Сарыкан', style_function=lambda x: {'color': 'blue'}).add_to(m)

# Добавление слоев управления
folium.LayerControl().add_to(m)

# Сохранение карты в файл
m.save("168.html")