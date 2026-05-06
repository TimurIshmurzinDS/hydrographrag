import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile strictly using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize folium.Map using the centroid of the basin shapefile
# Using 'CartoDB positron' tiles as requested
centroid = basin_gdf.geometry.centroid
map_center = [centroid.y.mean(), centroid.x.mean()]
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# 3. Add the basin boundary to the map with specific styling
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

# 4. Handling Coordinates (WKT)
# Since no specific WKT coordinates for sensors were provided in the context, 
# we define the logic for adding them if they were present.
# Example structure if coordinates were available:
# sensors_data = [
#     {"name": "Sarykan_Sensor_1", "coords": "POINT(x y)", "value": 120},
# ]
# for sensor in sensors_data:
#     point = wkt.loads(sensor["coords"])
#     folium.Marker([point.y, point.x], popup=f"{sensor['name']}: {sensor['value']}cm").add_to(m)

# 5. Save the final map strictly as "139.html"
m.save("139.html")