import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузка геоданных бассейна
# Используется raw-строка для пути к файлу. 
# Файл содержит только внешние границы полигона бассейна.
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Конвертация в стандартную географическую систему координат WGS84
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Инициализация карты
# Вычисляем центроид полигона бассейна для центрирования карты
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# 3. Добавление слоя бассейна на карту
# Согласно требованиям: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    basin_gdf, 
    fillColor='green', 
    color='darkgreen', 
    fillOpacity=0.2
).add_to(m)

# 4. Добавление координат объектов (если бы они были предоставлены в WKT в контексте)
# В данном контексте координаты WKT отсутствуют, поэтому список маркеров пуст.
coordinates_data = [] 
for point in coordinates_data:
    folium.Marker(
        location=[point['lat'], point['lon']], 
        popup=point['name']
    ).add_to(m)

# 5. Сохранение итоговой карты в строго определенный файл
m.save("6.html")