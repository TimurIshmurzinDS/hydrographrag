import geopandas as gpd
import folium
from shapely import wkt

# Загрузите shapefile бассейна реки Текес в гео-пандасе и преобразуйте его в систему координат EPSG:4326.
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создайте карту Folium с центром в середине бассейна и параметрами tiles='CartoDB positron'.
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавьте бассейн на карту как GeoJson.
folium.GeoJson(data=basin_gdf.to_json(), name='бассейн').add_child(folium.features.GeoJsonTooltip(fields=['name'], aliases=['Название'], labels=True)).add_to(m)

# Создайте список словарей для координат (WKT) реки Текес.
river_coords = [
    {'type': 'Point', 'coordinates': wkt.loads('POINT(45.123 30.456)').coords},
    {'type': 'LineString', 'coordinates': [[45.123, 30.456], [45.789, 30.012]]}
]

# Добавьте координаты реки Текес на карту.
folium.Marker(location=river_coords[0]['coordinates'], popup='Река Текес').add_to(m)
folium.PolyLine(locations=[point['coordinates'] for point in river_coords[1]['coordinates']], color='blue', weight=2).add_to(m)

# Сохраните карту в файл.
m.save("172.html")