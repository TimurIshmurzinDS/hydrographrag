import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile
# Using raw string for path as per instructions
gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system
gdf = gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin for map initialization
centroid = gdf.geometry.centroid
center_lat = centroid.y.mean()
center_lon = centroid.x.mean()

# Initialize folium map with specified tiles
m = folium.Map(
    location=[center_lat, center_lon], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# Add the basin boundary to the map with strict styling
folium.GeoJson(
    gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# Note: No WKT coordinates were provided in the context for the sensors, 
# so no hardcoded point list is added to the map.

# Save the final map strictly as 147.html
m.save("147.html")