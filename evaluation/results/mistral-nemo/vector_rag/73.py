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

# If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
observations = [
    {'type': 'Feature', 'geometry': wkt.loads('POINT(74.56 43.29)'), 'properties': {'name': '0.2 km above confluence with Osek River'}},
    {'type': 'Feature', 'geometry': wkt.loads('POINT(74.56 43.29)'), 'properties': {'name': '0.2 km above the confluence with Osek River'}},
    {'type': 'Feature', 'geometry': wkt.loads('POINT(74.56 43.29)'), 'properties': {'name': '0.2 km above the confluence with Osek River'}}
]

# Add observations to the map
for obs in observations:
    folium.Marker(location=[obs['geometry'].y, obs['geometry'].x], popup=obs['properties']['name']).add_to(m)

# Save the final map
m.save("73.html")