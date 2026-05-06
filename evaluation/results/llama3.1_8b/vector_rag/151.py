import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# 2. Создание карты с центром в середине бассейна
centroid = basin_data.centroid
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# 3. Добавление бассейна на карту
basin_geojson = basin_data.to_crs('EPSG:4326').to_json()
folium.GeoJson(basin_geojson,
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# 4. Создание списка точек с координатами (WKT)
wkt_points = [
    {"name": "Bayankol River", "geometry": wkt.loads("POINT(75.12345 46.67890)")},
    {"name": "Ili River", "geometry": wkt.loads("POINT(76.23456 47.89012)")}
]

# 5. Добавление точек на карту
for point in wkt_points:
    folium.Marker(point["geometry"].coords, popup=point["name"]).add_to(m)

# 6. Сохранение карты в файл
m.save("151.html")