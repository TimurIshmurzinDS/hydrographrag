import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границы бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты наблюдения (WKT)
observations = [
    {"name": "Observation 1", "geometry": wkt.loads("POINT(37.422 -122.084)")},
    {"name": "Observation 2", "geometry": wkt.loads("POINT(37.425 -122.086)")},
    {"name": "Observation 3", "geometry": wkt.loads("POINT(37.427 -122.088)")},
    {"name": "Observation 4", "geometry": wkt.loads("POINT(37.429 -122.090)")}
]

# Добавление точек наблюдения на карту
for obs in observations:
    folium.Marker([obs['geometry'].y, obs['geometry'].x], popup=obs['name']).add_to(m)

# Сохранение карты в файл
m.save("23.html")