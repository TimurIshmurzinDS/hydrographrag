import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile
# Using raw string for path as per instructions
gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 CRS
gdf = gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin for map initialization
centroid = gdf.geometry.centroid.iloc[0]

# Initialize folium map with specified tiles
m = folium.Map(
    location=[centroid.y, centroid.x], 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# Add the basin boundary to the map with strict styling
folium.GeoJson(
    gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# No WKT coordinates provided in the context for specific river points, 
# so no hardcoded point list is added.

# Save the final map strictly as 28.html
m.save("28.html")