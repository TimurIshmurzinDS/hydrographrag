import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
gdf = gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to initialize the map
centroid = gdf.geometry.centroid.iloc[0]
center_lat = centroid.y
center_lon = centroid.x

# Initialize folium Map using the centroid and specific tiles
m = folium.Map(
    location=[center_lat, center_lon], 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# Add the basin polygon to the map
# Strictly following the visual requirements: green fill, darkgreen border, 0.2 opacity
folium.GeoJson(
    gdf, 
    fillColor='green', 
    color='darkgreen', 
    fillOpacity=0.2
).add_to(m)

# Note: Context does not provide specific WKT coordinates for points, 
# so no hardcoded point list is added to avoid fabrication.

# Save the final map strictly using the required filename
m.save("278.html")