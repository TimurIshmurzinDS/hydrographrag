import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile
# Using raw string for path as per critical instructions
gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system
gdf = gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin for map initialization
centroid = gdf.geometry.centroid.iloc[0]

# Initialize the folium map centered on the basin
m = folium.Map(
    location=[centroid.y, centroid.x], 
    tiles='CartoDB positron', 
    zoom_start=6
)

# Add the basin boundary to the map
folium.GeoJson(
    gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# Note: No WKT coordinates were provided in the context for specific observation points.
# If coordinates were present, they would be added here as hardcoded markers.

# Save the final map strictly as 148.html
m.save("148.html")