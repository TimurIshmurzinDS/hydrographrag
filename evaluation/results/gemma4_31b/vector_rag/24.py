import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid
center_lat = centroid.y.mean()
center_lon = centroid.x.mean()

# Initialize the folium map with the specified tiles
m = folium.Map(
    location=[center_lat, center_lon], 
    zoom_start=12, 
    tiles='CartoDB positron'
)

# Add the basin boundary to the map
# Styling: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name='Ulken Almaty River Basin'
).add_to(m)

# Note: No WKT coordinates were provided in the context for the observation points.
# If coordinates were available, they would be added here as a list of dictionaries.

# Save the final map strictly as 24.html
m.save("24.html")