import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о пиковых уровнях воды (замените на реальные данные)
water_level_data = [
    {'year': 2015, 'value': 100},
    {'year': 2023, 'value': 120}
]

# Добавление точек с пиковыми уровнями воды на карту
for data in water_level_data:
    folium.Marker(
        location=[centroid.y, centroid.x],
        popup=f"Пиковый уровень в {data['year']}: {data['value']} м",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("49.html")