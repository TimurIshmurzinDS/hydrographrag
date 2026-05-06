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
posts = [
    {'name': 'Post 1', 'geometry': wkt.loads('POINT(45.123 78.901)')},
    {'name': 'Post 2', 'geometry': wkt.loads('POINT(45.234 78.892)')},
    {'name': 'Post 3', 'geometry': wkt.loads('POINT(45.345 78.883)')},
    {'name': 'Post 4', 'geometry': wkt.loads('POINT(45.456 78.874)')}
]

# Add posts to the map
for post in posts:
    folium.Marker(post['geometry'], popup=post['name']).add_to(m)

# Save the final map
m.save("78.html")