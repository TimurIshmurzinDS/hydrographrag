import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Hardcoded list of dictionaries for coordinates (WKT)
coordinates = [
    {'name': 'Датчик 1', 'status': 'Активен', 'geom': wkt.loads('POINT(74.65983 43.2043)')},
    {'name': 'Датчик 2', 'status': 'Неактивен', 'geom': wkt.loads('POINT(74.66123 43.2056)')}
]

# Add coordinates to the map
for coord in coordinates:
    folium.Marker(location=[coord['geom'].y, coord['geom'].x], popup=f"{coord['name']}: {coord['status']}").add_to(m)

# Save the final map
m.save("10.html")