import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы ровнинного участка на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных для текущего уровня воды и расхода воды (замените на реальные данные)
current_water_level = 150  # Уровень воды в метрах
water_consumption_value = 1000  # Текущий расход воды в м³

# Пороговые значения
threshold_level = 120  # Пороговый уровень воды
critical_level = 180  # Критический уровень воды

# Расчет индекса риска наводнения
if current_water_level < threshold_level:
    risk_index = 0
elif current_water_level > critical_level:
    risk_index = 1
else:
    risk_index = (current_water_level - threshold_level) / (critical_level - threshold_level)

# Добавление информации об индексе риска на карту
folium.Marker(
    location=[centroid.y, centroid.x],
    popup=f"Индекс риска наводнения: {risk_index:.2f}",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

# Сохранение карты в файл
m.save("30.html")