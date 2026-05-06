import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin for map initialization
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize folium map with the specified tiles
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# Add the basin boundary to the map
folium.GeoJson(
    basin_gdf,
    fillColor='green',
    color='darkgreen',
    fillOpacity=0.2,
    weight=2
).add_to(m)

# Note: No WKT coordinates were provided in the context for specific river points.
# If coordinates for the Koktal River observation point (0.2 km above Osek confluence) 
# were available, they would be added here as a hardcoded list of dictionaries.

# Save the final map strictly as 239.html
m.save("239.html")