import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузка пространственных данных бассейна
# Используется raw-строка для пути к файлу согласно инструкции
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# 2. Приведение системы координат к WGS84 (EPSG:4326) для совместимости с folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 3. Определение центральной точки бассейна для инициализации карты
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# 4. Инициализация карты с использованием тайлов CartoDB positron
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# 5. Добавление полигона бассейна на карту
# Параметры стиля: зеленый цвет заливки, темно-зеленый контур, прозрачность 0.2
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# 6. Сохранение итоговой карты в строго определенный файл
m.save("98.html")