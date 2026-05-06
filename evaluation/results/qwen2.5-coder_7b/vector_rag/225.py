import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка координат для черной дыры (пример)
black_hole_coords = [
    {"name": "Black Hole 1", "wkt": "POINT(76.945833 43.225)"},  # Пример WKT координат
    {"name": "Black Hole 2", "wkt": "POINT(76.950000 43.230)"}
]

# Добавление точек на карту
for coord in black_hole_coords:
    point = wkt.loads(coord["wkt"])
    folium.Marker([point.y, point.x], popup=coord["name"], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("225.html")