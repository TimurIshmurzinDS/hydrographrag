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

# Create a hardcoded list of dictionaries for coordinates (WKT)
observations = [
    {'type': 'Feature', 'geometry': wkt.loads('POINT(71.45 43.25)'), 'properties': {'name': 'Observation 1'}},
    {'type': 'Feature', 'geometry': wkt.loads('POINT(71.46 43.26)'), 'properties': {'name': 'Observation 2'}},
    {'type': 'Feature', 'geometry': wkt.loads('POINT(71.47 43.27)'), 'properties': {'name': 'Observation 3'}},
    {'type': 'Feature', 'geometry': wkt.loads('POINT(71.48 43.28)'), 'properties': {'name': 'Observation 4'}}
]

# Add observations to the map
for obs in observations:
    folium.Marker(location=[obs['geometry'].y, obs['geometry'].x], popup=obs['properties']['name']).add_to(m)

# Save the final map
m.save("24.html")