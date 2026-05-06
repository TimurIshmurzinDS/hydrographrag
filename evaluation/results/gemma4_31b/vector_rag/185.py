import geopandas as gpd
import folium
from shapely import wkt

# Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid
mean_lat = centroid.y.mean()
mean_lon = centroid.x.mean()

# Initialize folium Map
m = folium.Map(
    location=[mean_lat, mean_lon], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# Add the basin boundary to the map
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    tooltip="Basin Area: Byzhy River System"
).add_to(m)

# Note: No WKT coordinates were provided in the context for specific river points,
# so only the basin boundary is visualized.

# Save the final map strictly as 185.html
m.save("185.html")