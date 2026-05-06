import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центроиде водного бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты рек в формате WKT (для примера)
rivers = [
    {"name": "Tentek River", "geometry": wkt.loads("LINESTRING(35.1 48.2, 35.2 48.3)")},
    {"name": "Emel River", "geometry": wkt.loads("LINESTRING(35.0 48.0, 35.3 48.5)")},
    {"name": "Byzhy River", "geometry": wkt.loads("LINESTRING(34.9 47.9, 35.1 48.2)")}
]

# Добавление рек на карту
for river in rivers:
    folium.GeoJson({"type": "Feature", "properties": {"name": river["name"]}, "geometry": river["geometry"].__geo_interface__},
                     style_function=lambda x: {'color': 'blue', 'weight': 2}).add_to(m)

# Сохранение карты в файл
m.save("101.html")