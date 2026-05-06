import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
observations = [
    {'type': 'Observation', 'geometry': wkt.loads('POINT(37.56 55.74)')},
    {'type': 'Observation', 'geometry': wkt.loads('POINT(37.57 55.74)')},
    {'type': 'Observation', 'geometry': wkt.loads('POINT(37.58 55.74)')},
    {'type': 'Observation', 'geometry': wkt.loads('POINT(37.59 55.74)')}
]

# Add observations to the map
for obs in observations:
    folium.Marker(location=[obs['geometry'].y, obs['geometry'].x]).add_to(m)

# Save the final map
m.save("74.html")