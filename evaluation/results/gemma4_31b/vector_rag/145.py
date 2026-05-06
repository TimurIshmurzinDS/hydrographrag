import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 CRS for folium compatibility
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize the map
# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid
map_center = [centroid.y.mean(), centroid.x.mean()]

m = folium.Map(
    location=map_center, 
    zoom_start=6, 
    tiles='CartoDB positron'
)

# 3. Add the basin boundary to the map
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name="Basin Boundary"
).add_to(m)

# 4. Handle sensor coordinates
# Note: Context provided properties but no specific WKT coordinates.
# If WKT coordinates were provided in the context, they would be added here as a hardcoded list.
# Example structure if coordinates existed:
# sensors = [
#     {"name": "Sensor_1", "coords": "POINT(x y)", "level": "Value"},
# ]
# for s in sensors:
#     point = wkt.loads(s["coords"])
#     folium.Marker([point.y, point.x], popup=s["name"]).add_to(m)

# 5. Save the final map strictly as 145.html
m.save("145.html")