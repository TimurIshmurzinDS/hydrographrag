import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы ровнинного участка на карте
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат Добина Пира (если они доступны)
dobyn_pier_coords = [
    {"name": "Dobyn pier 1", "wkt": "POINT(37.422 -122.084)"},
    {"name": "Dobyn pier 2", "wkt": "POINT(37.425 -122.086)"},
    {"name": "Dobyn pier 3", "wkt": "POINT(37.427 -122.088)"}
]

# Добавление точек Добина Пира на карте
for pier in dobyn_pier_coords:
    point = wkt.loads(pier["wkt"])
    folium.Marker([point.y, point.x], popup=pier["name"]).add_to(m)

# Сохранение карты в файл
m.save("226.html")