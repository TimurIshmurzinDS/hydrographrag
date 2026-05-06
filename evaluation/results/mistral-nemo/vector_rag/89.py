import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = "EPSG:4326"

# Initialize Folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
observations = [
    {'name': 'Observation 1', 'geometry': wkt.loads('POINT(37.45 55.02)')},
    {'name': 'Observation 2', 'geometry': wkt.loads('POINT(37.46 55.03)')},
    {'name': 'Observation 3', 'geometry': wkt.loads('POINT(37.47 55.04)')}
]

# Add observations to the map
for obs in observations:
    folium.Marker(location=[obs['geometry'].y, obs['geometry'].x], popup=obs['name']).add_to(m)

# Save the final map
m.save("89.html")