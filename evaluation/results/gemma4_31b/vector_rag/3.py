import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузка данных о границах бассейна
# Используем raw-строку для пути к файлу, как указано в инструкции
basin_df = gpd.read_file(r"data/basin_data.shp")

# Конвертация в стандартную географическую систему координат WGS84 (EPSG:4326)
basin_df = basin_df.to_crs('EPSG:4326')

# 2. Инициализация карты
# Вычисляем центроид полигона бассейна для центрирования карты
centroid = basin_df.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# 3. Добавление слоя бассейна на карту
# Применяем строго заданные стили: зеленый цвет заливки, темно-зеленый контур, прозрачность 0.2
folium.GeoJson(
    basin_df, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# 4. Добавление координат объектов (если бы они были предоставлены в WKT в контексте)
# В данном контексте координаты отсутствуют, поэтому список остается пустым
observations = [] 
for obs in observations:
    folium.Marker(
        location=[obs['lat'], obs['lon']], 
        popup=obs['name']
    ).add_to(m)

# 5. Сохранение итоговой карты в строго определенный файл
m.save("3.html")