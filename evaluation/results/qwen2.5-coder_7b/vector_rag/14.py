import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре массы геометрии бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о уровнях воды (если доступны)
water_level_data = [
    {'date': '2023-10-01', 'value': 5.2, 'geometry': wkt.loads('POINT(37.4 55.6)')},
    {'date': '2023-10-02', 'value': 5.5, 'geometry': wkt.loads('POINT(37.5 55.7)')}
]

# Добавление маркеров с уровнями воды на карту
for data in water_level_data:
    folium.Marker(
        location=[data['geometry'].y, data['geometry'].x],
        popup=f"Уровень воды: {data['value']} м<br>Дата: {data['date']}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("14.html")