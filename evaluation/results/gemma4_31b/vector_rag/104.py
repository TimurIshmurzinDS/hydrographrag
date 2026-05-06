import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
gdf_basin = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
gdf_basin = gdf_basin.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = gdf_basin.geometry.centroid
center_lat = centroid.y.mean()
center_lon = centroid.x.mean()

# Initialize folium Map with the specified tiles
m = folium.Map(
    location=[center_lat, center_lon], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# Add the basin boundary to the map
folium.GeoJson(
    gdf_basin, 
    fillColor='green', 
    color='darkgreen', 
    fillOpacity=0.2
).add_to(m)

# Note: No WKT coordinates were provided in the context for the rivers, 
# so no additional point or line markers are added.

# Save the final map strictly as 104.html
m.save("104.html")