import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize the map centered on the basin centroid
m = folium.Map(location=basin.centroid.values[0], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Hardcoded list of posts (replace with actual data from database)
posts = [
    {'name': 'Post 1', 'coordinates': wkt.loads('POINT (68.54321 42.78901)')},
    {'name': 'Post 2', 'coordinates': wkt.loads('POINT (68.23456 42.56789)')}
]

# Add markers for each post to the map
for post in posts:
    folium.Marker(location=[post['coordinates'].y, post['coordinates'].x], popup=post['name']).add_to(m)

# Save the map
m.save("88.html")