import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize the folium map
# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid
mean_lat = centroid.y.mean()
mean_lon = centroid.x.mean()

m = folium.Map(
    location=[mean_lat, mean_lon], 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 3. Add the basin boundary to the map
# Using the specified colors and opacity
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name="Urzhar River Basin"
).add_to(m)

# 4. Handle coordinates if they were provided as WKT in the context
# Since no specific WKT coordinates were provided in the prompt's context, 
# we skip adding point markers to avoid creating dummy data.
# If coordinates were present, they would be added here as a list of dictionaries.

# 5. Save the final map strictly as 195.html
m.save("195.html")