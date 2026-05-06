import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system for web mapping
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize the folium map with the specified tiles
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=12)

# Add the basin polygon to the map
# Using specified colors and opacity for professional GIS representation
folium.GeoJson(
    basin_gdf,
    fillColor='green',
    color='darkgreen',
    fillOpacity=0.2,
    popup='Basin of Batareyka River'
).add_to(m)

# Note: No WKT coordinates were provided in the context for the observation point.
# If coordinates were available, they would be added here as a list of dictionaries.

# Save the final map strictly as 220.html
m.save("220.html")