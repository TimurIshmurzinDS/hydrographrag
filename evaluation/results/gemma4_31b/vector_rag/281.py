import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile using a raw string as per strict instructions
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to initialize the map center
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize folium Map with CartoDB positron tiles
m = folium.Map(location=map_center, zoom_start=10, tiles='CartoDB positron')

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
    tooltip="Hydrological Basin Boundary"
).add_to(m)

# Note: Context does not provide specific WKT coordinates for points, 
# so no hardcoded point list is added to avoid hallucination.

# Save the final map strictly using the required filename
m.save("281.html")