import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile
# The file contains only the exterior polygon boundaries of the basin
gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system
gdf = gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin for map initialization
centroid = gdf.geometry.centroid.iloc[0]
center_lat = centroid.y
center_lon = centroid.x

# Initialize the folium map with the specified tiles
m = folium.Map(
    location=[center_lat, center_lon], 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# Add the basin polygon to the map
# Using strict styling: green fill, darkgreen border, 0.2 opacity
folium.GeoJson(
    gdf, 
    fillColor='green', 
    color='darkgreen', 
    fillOpacity=0.2
).add_to(m)

# Save the final map strictly as 255.html
m.save("255.html")