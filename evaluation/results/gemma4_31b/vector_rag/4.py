import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
gdf_basin = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system
gdf_basin = gdf_basin.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = gdf_basin.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize the folium map with the specified tiles
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# Add the basin boundary to the map
folium.GeoJson(
    gdf_basin,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# Note: No WKT coordinates were provided in the context for the rivers or stations,
# so no hardcoded point markers are added.

# Save the final map strictly as 4.html
m.save("4.html")