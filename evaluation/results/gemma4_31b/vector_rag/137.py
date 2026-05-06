import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basins
gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
gdf = gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basins to initialize the map center
centroid = gdf.geometry.centroid
mean_lat = centroid.y.mean()
mean_lon = centroid.x.mean()

# Initialize folium Map with CartoDB positron tiles
m = folium.Map(location=[mean_lat, mean_lon], tiles='CartoDB positron', zoom_start=6)

# Add the basin boundaries to the map
# Using specified colors: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# Note: No WKT coordinates for sensors were provided in the context.
# If coordinates were present, they would be added here as folium.Marker.

# Save the final map strictly as 137.html
m.save("137.html")