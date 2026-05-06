import geopandas as gpd
import folium
from shapely import wkt

# Загрузите shapefile с использованием raw string и преобразуйте в CRS 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создайте карту Folium с центром в середине области
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавьте область на карту
folium.GeoJson(data=basin_gdf.to_json(), name='basin').add_to(m)

# Создайте список словарей для координат (WKT), если они есть
wkt_coords = [
    {'lat': 43.1234, 'lon': 76.5432},
    {'lat': 43.1245, 'lon': 76.5443}
]

# Добавьте точки на карту
for coord in wkt_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранитe карту в файле с именем '61.html'
m.save("61.html")