import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с границами бассейна
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создать карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(data=basin_gdf.to_json(), name='basin').add_to(m)

# Создать список словарей с координатами (WKT) для рек Tekes River и Bayankol River
river_coords = [
    {'name': 'Tekes River', 'wkt': wkt.loads('POLYGON ((...))')},
    {'name': 'Bayankol River', 'wkt': wkt.loads('POLYGON ((...))')}
]

# Добавить реки на карту
for river in river_coords:
    folium.GeoJson(data=river['wkt'].to_json(), name=river['name']).add_to(m)

# Сохранить карту в файл
m.save("25.html")