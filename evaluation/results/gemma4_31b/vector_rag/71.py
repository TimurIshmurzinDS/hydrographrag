import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid
center_lat = centroid.y.mean()
center_lon = centroid.x.mean()

# Initialize folium Map with the specified tiles
m = folium.Map(
    location=[center_lat, center_lon], 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# Add the basin boundary to the map
folium.GeoJson(
    basin_gdf, 
    fillColor='green', 
    color='darkgreen', 
    fillOpacity=0.2
).add_to(m)

# Note: No coordinates (WKT) were provided in the context for specific sensors.
# If coordinates were provided, they would be added here as a hardcoded list of dictionaries.

# Save the final map strictly as 71.html
m.save("71.html")