import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы ровнинного участка на карте
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных по уровням воды и потреблению воды (замените на реальные данные)
water_level_data = [
    {'date': '2023-10-01', 'level_cm': 50, 'consumption': 100},
    {'date': '2023-10-02', 'level_cm': 60, 'consumption': 150},
    {'date': '2023-10-03', 'level_cm': 70, 'consumption': 200}
]

# Критическая отметка паводка (замените на реальное значение)
critical_water_level = 65

# Проверка превышения критической отметки
for data in water_level_data:
    if data['level_cm'] > critical_water_level:
        print(f"На {data['date']} уровень воды превысил критическую отметку: {data['level_cm']} см")

# Сохранение финальной карты
m.save("82.html")