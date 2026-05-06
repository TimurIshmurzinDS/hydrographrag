import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundaries from the shapefile
# The file contains only the exterior polygon boundaries of the basins
gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system for mapping
gdf = gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basins to center the map
centroid = gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize the folium map with the specified tiles
m = folium.Map(
    location=map_center, 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# Add the basin polygons to the map
# Using the required styling: green fill, darkgreen border, 0.2 opacity
folium.GeoJson(
    gdf, 
    fillColor='green', 
    color='darkgreen', 
    fillOpacity=0.2
).add_to(m)

# Save the final map to the strictly required filename
m.save("177.html")