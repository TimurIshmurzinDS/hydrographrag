import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка точек наблюдения (WKT)
observations = [
    {"name": "Observation 1", "wkt": "POINT(37.422 -122.084)"},
    {"name": "Observation 2", "wkt": "POINT(37.425 -122.086)"},
    {"name": "Observation 3", "wkt": "POINT(37.427 -122.088)"},
    {"name": "Observation 4", "wkt": "POINT(37.429 -122.090)"}
]

# Преобразование WKT в объекты shapely
observation_points = [wkt.loads(obs["wkt"]) for obs in observations]

# Добавление точек наблюдения на карту
for point in observation_points:
    folium.Marker([point.y, point.x], popup=point.wkt).add_to(m)

# Сохранение карты в файл "5.html"
m.save("5.html")