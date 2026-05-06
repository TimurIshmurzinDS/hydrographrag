import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Шынжалы
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs(epsg=4326)

# Инициализация карты с использованием центроида бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть данные о водном уровне для рек Шынжалы и Шилик в формате WKT
# Создание списка словарей с координатами и значениями уровня воды
water_level_data = [
    {'geometry': wkt.loads('POINT(76.92307 43.18566)'), 'value': 120},  # Примерные координаты для Шынжалы Реки
    {'geometry': wkt.loads('POINT(76.92307 43.18566)'), 'value': 130},  # Примерные координаты для Шынжалы Реки
    {'geometry': wkt.loads('POINT(76.92307 43.18566)'), 'value': 140},  # Примерные координаты для Шынжалы Реки
    {'geometry': wkt.loads('POINT(76.92307 43.18566)'), 'value': 150},  # Примерные координаты для Шынжалы Реки
    {'geometry': wkt.loads('POINT(76.92307 43.18566)'), 'value': 160},  # Примерные координаты для Шынжалы Реки
    {'geometry': wkt.loads('POINT(76.92307 43.18566)'), 'value': 170},  # Примерные координаты для Шынжалы Реки
    {'geometry': wkt.loads('POINT(76.92307 43.18566)'), 'value': 180},  # Примерные координаты для Шынжалы Реки
    {'geometry': wkt.loads('POINT(76.92307 43.18566)'), 'value': 190},  # Примерные координаты для Шынжалы Реки
    {'geometry': wkt.loads('POINT(76.92307 43.18566)'), 'value': 200},  # Примерные координаты для Шынжалы Реки
    {'geometry': wkt.loads('POINT(76.92307 43.18566)'), 'value': 120},  # Примерные координаты для Шилик Реки
    {'geometry': wkt.loads('POINT(76.92307 43.18566)'), 'value': 130},  # Примерные координаты для Шилик Реки
    {'geometry': wkt.loads('POINT(76.92307 43.18566)'), 'value': 140},  # Примерные координаты для Шилик Реки
    {'geometry': wkt.loads('POINT(76.92307 43.18566)'), 'value': 150},  # Примерные координаты для Шилик Реки
    {'geometry': wkt.loads('POINT(76.92307 43.18566)'), 'value': 160},  # Примерные координаты для Шилик Реки
    {'geometry': wkt.loads('POINT(76.92307 43.18566)'), 'value': 170},  # Примерные координаты для Шилик Реки
    {'geometry': wkt.loads('POINT(76.92307 43.18566)'), 'value': 180},  # Примерные координаты для Шилик Реки
    {'geometry': wkt.loads('POINT(76.92307 43.18566)'), 'value': 190},  # Примерные координаты для Шилик Реки
    {'geometry': wkt.loads('POINT(76.92307 43.18566)'), 'value': 200}   # Примерные координаты для Шилик Реки
]

# Добавление точек с уровнями воды на карту
for point in water_level_data:
    folium.CircleMarker(
        location=[point['geometry'].y, point['geometry'].x],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        popup=f"Уровень воды: {point['value']} м"
    ).add_to(m)

# Сохранение карты в файл
m.save("161.html")