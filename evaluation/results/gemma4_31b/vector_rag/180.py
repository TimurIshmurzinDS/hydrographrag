import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_df = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system
basin_df = basin_df.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = basin_df.geometry.centroid
center_lat = centroid.y.iloc[0]
center_lon = centroid.x.iloc[0]

# Initialize folium map with the specified tile set
m = folium.Map(
    location=[center_lat, center_lon], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# Add the basin boundary to the map
folium.GeoJson(
    basin_df, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2, 
        'weight': 2
    }
).add_to(m)

# Note: No WKT coordinates were provided in the context for the observation points.
# If coordinates were present, they would be added here as a hardcoded list of dictionaries.

# Save the final map strictly as 180.html
m.save("180.html")