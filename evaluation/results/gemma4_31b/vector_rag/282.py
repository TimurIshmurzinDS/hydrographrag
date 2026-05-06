import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile
# Using raw string for path as per critical instructions
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system for folium compatibility
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize the folium map with the specified tile set
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# Add the basin boundary to the map
# Strictly following the color and opacity requirements
folium.GeoJson(
    basin_gdf,
    fillColor='green',
    color='darkgreen',
    fillOpacity=0.2
).add_to(m)

# Note: No points or river names are read from the shapefile to avoid fatal errors.
# If WKT coordinates were provided in the context, they would be added here as markers.

# Save the final map strictly using the required filename
m.save("282.html")