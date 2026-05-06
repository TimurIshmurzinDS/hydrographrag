import geopandas as gpd
import folium
from shapely import wkt

# Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize folium Map with CartoDB positron tiles
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=12)

# Add the basin boundary to the map
# Styling: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    basin_gdf,
    fillColor='green',
    color='darkgreen',
    fillOpacity=0.2,
    weight=2
).add_to(m)

# Note: The context mentions observation points 0.2 km above the confluence, 
# but no specific WKT coordinates were provided in the input context.
# Therefore, no hardcoded point markers are added.

# Save the final map strictly as 238.html
m.save("238.html")