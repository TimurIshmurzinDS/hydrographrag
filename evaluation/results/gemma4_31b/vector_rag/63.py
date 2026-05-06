import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузка данных о границах бассейна
# Используется raw-строка для пути к файлу, согласно инструкции
basin_df = gpd.read_file(r"data/basin_data.shp")

# Конвертация в стандартную географическую систему координат WGS84
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
# Применяются строго заданные параметры стилизации: зеленый цвет, прозрачность 0.2
folium.GeoJson(
    basin_df, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# 4. Обработка координат гидропостов
# В предоставленном контексте WKT координаты отсутствуют, 
# поэтому список маркеров остается пустым. 
# Если бы координаты были предоставлены, они были бы добавлены здесь.
coords_list = [] 
for point in coords_list:
    folium.Marker(
        location=[point['lat'], point['lon']], 
        popup=point['info']
    ).add_to(m)

# 5. Сохранение итоговой карты в строго определенный файл
m.save("63.html")