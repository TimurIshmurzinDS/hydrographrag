import geopandas as gpd
import folium
from shapely import wkt

# Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid
center_lat = centroid.y.iloc[0]
center_lon = centroid.x.iloc[0]

# Initialize folium map with specified tiles
m = folium.Map(
    location=[center_lat, center_lon], 
    tiles='CartoDB positron', 
    zoom_start=10
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

# The context does not provide specific WKT coordinates for the observations, 
# so no additional point markers are added to avoid fabrication.

# Save the final map strictly as 248.html
m.save("248.html")