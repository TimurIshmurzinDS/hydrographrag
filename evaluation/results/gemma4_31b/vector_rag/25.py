import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile
# Using raw string for path as per critical instructions
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
    zoom_start=10, 
    tiles='CartoDB positron'
)

# Add the basin boundary to the map with strict styling
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name='Basin Boundary'
).add_to(m)

# Note: Context did not provide specific WKT coordinates for the rivers or village.
# If coordinates were provided, they would be added here as folium.Marker.

# Save the final map strictly as 25.html
m.save("25.html")