import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile и параметрами tiles='CartoDB positron'
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о потреблении воды и уровне воды (замените на реальные данные)
water_consumption_data = [
    {'river': 'Prokhodnaya River', 'season': 'winter', 'consumption': 100},
    {'river': 'Prokhodnaya River', 'season': 'spring', 'consumption': 200},
    {'river': 'Prokhodnaya River', 'season': 'summer', 'consumption': 300},
    {'river': 'Prokhodnaya River', 'season': 'autumn', 'consumption': 150},
    {'river': 'Baskan River', 'season': 'winter', 'consumption': 80},
    {'river': 'Baskan River', 'season': 'spring', 'consumption': 180},
    {'river': 'Baskan River', 'season': 'summer', 'consumption': 280},
    {'river': 'Baskan River', 'season': 'autumn', 'consumption': 130}
]

# Прогнозирование уровня воды на весеннем половодье
spring_consumption_prokhodnaya = [d['consumption'] for d in water_consumption_data if d['river'] == 'Prokhodnaya River' and d['season'] == 'spring']
spring_consumption_baskan = [d['consumption'] for d in water_consumption_data if d['river'] == 'Baskan River' and d['season'] == 'spring']

predicted_water_level_prokhodnaya = sum(spring_consumption_prokhodnaya) / len(spring_consumption_prokhodnaya)
predicted_water_level_baskan = sum(spring_consumption_baskan) / len(spring_consumption_baskan)

print(f"Прогнозируемый уровень воды на весеннем половодье на Prokhodnaya River: {predicted_water_level_prokhodnaya} m³")
print(f"Прогнозируемый уровень воды на весеннем половодье на Baskan River: {predicted_water_level_baskan} m³")

# Сохранение карты
m.save("77.html")