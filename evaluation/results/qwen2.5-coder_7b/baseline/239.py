import folium
import geopandas as gpd

# Загрузка данных уровня реки Коктал (пример использования GeoJSON)
# Предположим, что файл level_koktala.geojson содержит данные о реке Коктал
gdf = gpd.read_file('level_koktala.geojson')

# Создание базовой карты
m = folium.Map(location=[50.45, 30.52], zoom_start=10)

# Добавление уровня реки Коктал на карту
folium.GeoJson(gdf).add_to(m)

# Добавление маркеров в космос (пример)
folium.Marker([50.45, 30.52], popup='Планета Земля').add_to(m)
folium.Marker([50.46, 30.53], popup='Астероид').add_to(m)

# Сохранение карты
m.save("239.html")