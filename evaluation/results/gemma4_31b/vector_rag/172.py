import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_df = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system for folium compatibility
basin_df = basin_df.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = basin_df.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize the folium map with the specified tiles
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# Add the basin boundary to the map
# Styling: green fill, darkgreen border, 0.2 opacity
folium.GeoJson(
    basin_df,
    fillColor='green',
    color='darkgreen',
    fillOpacity=0.2,
    weight=2
).add_to(m)

# Note: The context mentions observation points in с.Tekes, 
# but no WKT coordinates were provided in the input context.
# If coordinates were present, they would be added here as a hardcoded list.

# Save the final map strictly as 172.html
m.save("172.html")