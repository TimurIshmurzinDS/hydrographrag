import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile
# Using raw string for path as per critical instructions
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin for map initialization
centroid = basin_gdf.geometry.centroid
map_center = [centroid.y.iloc[0], centroid.x.iloc[0]]

# Initialize the folium map with specified tiles
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# Add the basin boundary to the map with strict styling
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# The context does not provide WKT coordinates for the sensors, 
# so no hardcoded point list is added to avoid fabrication.

# Save the final map strictly as 68.html
m.save("68.html")