import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize the folium map with the specified tiles
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=12)

# Add the basin boundary to the map with strict styling requirements
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    tooltip="Agricultural Basin: Temirlik and Byzhy Rivers"
).add_to(m)

# Note: Coordinates for Temirlik village and rivers are not provided in WKT format 
# in the context, so they are not added as hardcoded markers.

# Save the final map strictly as 115.html
m.save("115.html")