import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundaries shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system
gdf = gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = gdf.geometry.centroid.iloc[0]
center_lat = centroid.y
center_lon = centroid.x

# Initialize the folium map with the specified tiles
m = folium.Map(
    location=[center_lat, center_lon], 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# Add the basin boundary to the map
# Using the required styling: green fill, darkgreen border, 0.2 opacity
folium.GeoJson(
    gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2, 
        'weight': 2
    }
).add_to(m)

# Note: Context provided entities (Lepsy River, Turgen River, аул Lepsy) 
# but did not provide specific WKT coordinates for them. 
# If coordinates were provided, they would be added here as markers.

# Save the final map strictly as 198.html
m.save("198.html")