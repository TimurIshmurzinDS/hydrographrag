import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о текущих уровнях воды (WKT)
water_level_points = [
    {'geometry': wkt.loads('POINT(37.123456 55.678901)'), 'value': 0.2},
    {'geometry': wkt.loads('POINT(37.123457 55.678902)'), 'value': 0.3}
]

# Добавление точек с уровнями воды на карту
for point in water_level_points:
    folium.CircleMarker(
        location=[point['geometry'].y, point['geometry'].x],
        radius=10,
        color='blue',
        fill=True,
        fill_color='blue',
        popup=f'Уровень воды: {point["value"]} km'
    ).add_to(m)

# Сохранение карты
m.save("55.html")