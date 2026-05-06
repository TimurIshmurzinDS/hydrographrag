import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре массы бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о водных уровнях (если они доступны)
water_level_data = [
    {'geometry': wkt.loads('POINT(123.456 78.901)'), 'Water_level_Valuecm': 10},
    {'geometry': wkt.loads('POINT(123.457 78.902)'), 'Water_level_Valuecm': 15}
]

# Добавление точек с водными уровнями на карту
for point in water_level_data:
    folium.Marker(
        location=[point['geometry'].y, point['geometry'].x],
        popup=f"Водный уровень: {point['Water_level_Valuecm']} см",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("233.html")