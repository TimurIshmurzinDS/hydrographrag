import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_df = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_df = basin_df.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = basin_df.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize folium Map with the specified tiles
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# Add the basin boundary to the map
# Using specified colors and opacity for the hydro-basin representation
folium.GeoJson(
    basin_df,
    fillColor='green',
    color='darkgreen',
    fillOpacity=0.2,
    weight=2
).add_to(m)

# Note: No WKT coordinates were provided in the context for the rivers, 
# so only the basin boundary is visualized.

# Save the final map strictly as 178.html
m.save("178.html")