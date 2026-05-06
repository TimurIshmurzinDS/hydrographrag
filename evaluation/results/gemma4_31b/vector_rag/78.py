import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# 2. Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 3. Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# 4. Initialize folium Map with specified tiles
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# 5. Add the basin boundary to the map with strict styling
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# 6. Hardcoded observation points based on context (Temirlik village)
# Note: Since specific WKT coordinates were not provided in the context, 
# we represent the observation posts as a conceptual list. 
# If coordinates were present, they would be added here.
observation_points = [
    {"name": "Temirlik village Post 1", "type": "Observation"},
    {"name": "Temirlik village Post 2", "type": "Observation"},
    {"name": "Temirlik village Post 3", "type": "Observation"},
    {"name": "Temirlik village Post 4", "type": "Observation"},
]

# (Optional) If coordinates were available, we would iterate and add markers here.
# For this specific task, we visualize the basin area where these posts are located.

# 7. Save the final map strictly as "78.html"
m.save("78.html")