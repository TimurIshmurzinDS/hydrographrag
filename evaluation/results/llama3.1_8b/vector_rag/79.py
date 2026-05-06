import geopandas as gpd
import folium
from shapely import wkt

# Загрузите shapefile с внешними границами бассейна
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf.crs = 'EPSG:4326'

# Создайте карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавьте бассейн на карту
folium.GeoJson(basin_gdf.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создайте список словарей с координатами (WKT) для реки Turgen River
turgen_coords = [
    {'lat': 43.1234, 'lon': 79.5678},
    {'lat': 43.2345, 'lon': 79.6789}
]

# Добавьте точки на карту
for coord in turgen_coords:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохраните карту в файл
m.save("79.html")