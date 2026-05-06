import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна и преобразование в CRS EPSG:4326
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs(epsg=4326)

# Инициализация карты с центром по центроиду бассейна
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление границ бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположительные координаты точки наблюдения для Каратал (1.1 км выше Улькен Алматы)
# И предположительная точка впадения реки Улькен Алматы
points = [
    {"name": "Observation Point Karatal", "geometry": wkt.loads("POINT(76.92305 42.88417)")},  # Примерные координаты
    {"name": "Inflow Point Ulken Almaty", "geometry": wkt.loads("POINT(76.92305 42.87417)")}  # Примерные координаты
]

# Добавление точек на карту
for point in points:
    folium.Marker(
        location=[point['geometry'].y, point['geometry'].x],
        popup=point['name'],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("102.html")