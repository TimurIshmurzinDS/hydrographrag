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

# Create a hardcoded list of dictionaries with coordinates of sensors (if available in context)
sensors = [
    {'name': 'Sensor 1', 'geometry': wkt.loads('POINT(51.5074 -0.1278)')},
    {'name': 'Sensor 2', 'geometry': wkt.loads('POINT(51.5156 -0.1392)')}
]

# Add sensors to the map
for sensor in sensors:
    folium.Marker(sensor['geometry'], popup=sensor['name']).add_to(m)

# Save the final map
m.save("147.html")