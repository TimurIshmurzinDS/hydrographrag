import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize Folium map centered on the basin centroid
m = folium.Map(location=basin.centroid.values[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Define hardcoded list of post coordinates (replace with actual data)
posts = [
    {'coordinates': wkt.loads('POINT (43.1234 56.7890)'), 'flow_rate': 150},
    {'coordinates': wkt.loads('POINT (43.5678 57.9012)'), 'flow_rate': 200}
]

# Add posts to the map and highlight those exceeding critical flow rate
for post in posts:
    folium.Marker(location=[post['coordinates'].y, post['coordinates'].x], popup=f'Flow Rate: {post["flow_rate"]}').add_to(m)

# Save the map
m.save("82.html")