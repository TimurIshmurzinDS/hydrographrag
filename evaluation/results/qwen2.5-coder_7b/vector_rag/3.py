import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для визуализации)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о уровне воды (замените на реальные данные)
water_level_data = [
    {'date': '2023-10-01', 'level': 5.2},
    {'date': '2023-10-02', 'level': 5.4},
    {'date': '2023-10-03', 'level': 5.6}
]

# Нахождение последнего показателя уровня воды
last_water_level = max(water_level_data, key=lambda x: x['date'])
print(f"Последний показатель уровня воды на реке Talgar River: {last_water_level['level']} м")

# Сохранение карты
m.save("3.html")