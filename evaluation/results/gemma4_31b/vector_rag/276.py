import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile
# The file contains only the exterior polygon boundaries of the basin
basin_df = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system
basin_df = basin_df.to_crs('EPSG:4326')

# Calculate the centroid of the basin for map initialization
centroid = basin_df.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize folium map with specified tiles
m = folium.Map(location=map_center, zoom_start=10, tiles='CartoDB positron')

# Add the basin boundary to the map
folium.GeoJson(
    basin_df,
    fillColor='green',
    color='darkgreen',
    fillOpacity=0.2,
    popup='Basin Boundary'
).add_to(m)

# Note: Context contains Observation entities but no specific WKT coordinates.
# If coordinates were provided, they would be added here as a list of dictionaries.

# Save the final map strictly as 276.html
m.save("276.html")