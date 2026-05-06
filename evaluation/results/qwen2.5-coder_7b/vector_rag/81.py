import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реках и их уровни воды
rivers = {
    "Baskan River": 10,  # Примерный уровень воды на Baskan River (в метрах)
    "Prokhodnaya River": 8  # Примерный уровень воды на Prokhodnaya River (в метрах)
}

# Загрузка границы бассейна из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центре бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Определение нормальных уровней воды для каждой реки (примерные значения)
normal_levels = {
    "Baskan River": 12,
    "Prokhodnaya River": 10
}

# Сравнение текущих уровней воды с нормальными и определение превышений
for river, current_level in rivers.items():
    if current_level > normal_levels[river]:
        folium.Marker([centroid.y, centroid.x], popup=f"{river} - Уровень воды превышает норму", icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("81.html")