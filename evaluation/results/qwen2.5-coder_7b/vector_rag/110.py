import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для контекста)
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

# Пример данных по потреблению воды (замените на реальные данные)
water_consumption_data = [
    {'name': 'Sarykan River', 'value': 15000},  # В кубических метрах в год
    {'name': 'Tekeli River', 'value': 2000}   # В кубических метрах в год
]

# Добавление точек на карте с данными по потреблению воды
for item in water_consumption_data:
    folium.Marker(
        location=[centroid.y, centroid.x],
        popup=f"{item['name']}: {item['value']} м³/год",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("110.html")