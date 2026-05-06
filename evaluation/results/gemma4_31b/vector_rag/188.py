import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile using a raw string as per critical instructions
# The file contains only the exterior polygon boundaries of the basins
gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
gdf = gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin polygons to center the map
centroid = gdf.geometry.centroid
mean_lat = centroid.y.mean()
mean_lon = centroid.x.mean()

# Initialize folium Map with the specified tiles
m = folium.Map(
    location=[mean_lat, mean_lon], 
    zoom_start=6, 
    tiles='CartoDB positron'
)

# Add the basin boundaries to the map
# Using the required styling: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# Note: No specific WKT coordinates for river points were provided in the context.
# If coordinates were provided, they would be added here as a hardcoded list of dictionaries.

# Save the final map strictly using the required filename
m.save("188.html")