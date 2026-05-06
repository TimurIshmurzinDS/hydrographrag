import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system for folium compatibility
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid.iloc[0]
center_lat = centroid.y
center_lon = centroid.x

# Initialize the folium map with the specified tiles
m = folium.Map(
    location=[center_lat, center_lon], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# Add the basin boundary to the map
# Using professional GIS styling: green fill and darkgreen borders
folium.GeoJson(
    basin_gdf, 
    fillColor='green', 
    color='darkgreen', 
    fillOpacity=0.2
).add_to(m)

# Save the final map strictly as 251.html
m.save("251.html")