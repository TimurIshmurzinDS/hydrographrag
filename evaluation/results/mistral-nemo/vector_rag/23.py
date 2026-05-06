import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
observations = [
    {'type': 'Observation', 'location': wkt.loads('POINT(37.56 55.74)')},
    {'type': 'Observation', 'location': wkt.loads('POINT(37.55 55.74)')},
    {'type': 'Observation', 'location': wkt.loads('POINT(37.54 55.74)')},
    {'type': 'Observation', 'location': wkt.loads('POINT(37.53 55.74)')}
]

# Add observations to the map
for obs in observations:
    folium.Marker(location=[obs['location'].y, obs['location'].x], popup=obs['type']).add_to(m)

# Save the final map
m.save("23.html")