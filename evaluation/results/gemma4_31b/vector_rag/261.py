import geopandas as gpd
import folium
from shapely import wkt

# Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
gdf = gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = gdf.geometry.centroid.iloc[0]
center_lat = centroid.y
center_lon = centroid.x

# Initialize folium Map with the specified tiles
m = folium.Map(
    location=[center_lat, center_lon], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# Add the basin boundary to the map
folium.GeoJson(
    gdf, 
    fillColor='green', 
    color='darkgreen', 
    fillOpacity=0.2
).add_to(m)

# Note: The context mentions a point 0.2 km above the confluence, 
# but no specific WKT coordinates were provided in the input.
# If coordinates were available, they would be added here as a hardcoded list.

# Save the final map strictly as 261.html
m.save("261.html")