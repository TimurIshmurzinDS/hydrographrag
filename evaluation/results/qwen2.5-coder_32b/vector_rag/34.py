import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Лепси
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Лепси
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о загрязнении воды (координаты и класс качества)
water_quality_data = [
    {"coordinates": "POINT(37.618423 55.755826)", "quality_class": "загрязненная"},
    {"coordinates": "POINT(37.620423 55.757826)", "quality_class": "чистая"},
    {"coordinates": "POINT(37.619423 55.756826)", "quality_class": "загрязненная"}
]

# Добавление точек на карту с учетом класса качества воды
for point in water_quality_data:
    coordinates = wkt.loads(point["coordinates"]).coords[0]
    quality_color = 'red' if point["quality_class"] == "загрязненная" else 'blue'
    folium.CircleMarker(location=[coordinates[1], coordinates[0]], radius=5, color=quality_color, fill=True, fillOpacity=0.6).add_to(m)

# Сохранение карты в файл
m.save("34.html")