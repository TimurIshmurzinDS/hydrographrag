import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузка данных о границах бассейна
# Используем raw-строку для пути к файлу, как указано в инструкции
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Конвертация в стандартную географическую систему координат WGS84
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Инициализация карты
# Вычисляем центроид бассейна для центрирования карты
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    zoom_start=12, 
    tiles='CartoDB positron'
)

# 3. Визуализация бассейна
# Добавление полигона бассейна с заданными параметрами оформления
folium.GeoJson(
    basin_gdf, 
    fillColor='green', 
    color='darkgreen', 
    fillOpacity=0.2
).add_to(m)

# 4. Обработка координат (WKT)
# В предоставленном контексте WKT-координаты отсутствуют, 
# поэтому список объектов остается пустым для предотвращения ошибок.
points_to_plot = []

for point in points_to_plot:
    folium.Marker(
        location=[point['lat'], point['lon']], 
        popup=point['name']
    ).add_to(m)

# 5. Сохранение итоговой карты в строго определенный файл
m.save("102.html")