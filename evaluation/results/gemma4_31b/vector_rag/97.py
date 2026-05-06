import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid.iloc[0]

# Initialize the folium map with the specified tiles
m = folium.Map(
    location=[centroid.y, centroid.x], 
    zoom_start=8, 
    tiles='CartoDB positron'
)

# Add the basin boundary to the map with strict styling
folium.GeoJson(
    basin_gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# Note: No WKT coordinates were provided in the context for the rivers, 
# so no hardcoded point/line dictionaries are added.

# Save the final map strictly as 97.html
m.save("97.html")