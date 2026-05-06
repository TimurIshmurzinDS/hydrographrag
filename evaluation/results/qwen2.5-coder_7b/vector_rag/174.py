import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с использованием центра масс shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границы ровнинного участка на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка точек пересечения (WKT)
intersection_points = [
    {"name": "Point 1", "geometry": wkt.loads("POINT(37.5642 55.0987)")},
    {"name": "Point 2", "geometry": wkt.loads("POINT(37.5642 55.0987)")},
    {"name": "Point 3", "geometry": wkt.loads("POINT(37.5642 55.0987)")}
]

# Добавление точек пересечения на карту
for point in intersection_points:
    folium.Marker([point["geometry"].y, point["geometry"].x], popup=point["name"], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("174.html")