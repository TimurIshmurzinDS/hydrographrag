import geopandas as gpd
import folium
from shapely import wkt

# Загрузите shapefile с бассейном
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf.crs = 'EPSG:4326'

# Создайте карту Folium с центром в середине бассейна
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавьте бассейн на карту
folium.GeoJson(basin_gdf.to_crs(epsg=3857).geometry.apply(lambda x: wkt.dumps(x)).tolist(),
               name='Basin',
               style_function=lambda feature: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создайте список словарей с координатами (WKT)
coordinates = [
    {"lat": 43.1234, "lon": 76.5432},
    {"lat": 44.1234, "lon": 77.5432},
    {"lat": 45.1234, "lon": 78.5432}
]

# Добавьте координаты на карту
folium.Marker([43.1234, 76.5432], popup='Координата 1').add_to(m)
folium.Marker([44.1234, 77.5432], popup='Координата 2').add_to(m)
folium.Marker([45.1234, 78.5432], popup='Координата 3').add_to(m)

# Сохраните карту в файл
m.save("227.html")