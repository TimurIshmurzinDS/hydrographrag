import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the shapefile using a raw string and convert to EPSG:4326
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize folium Map using the centroid of the basin shapefile
# Using 'CartoDB positron' tiles as requested
centroid = basin_gdf.geometry.centroid
map_center = [centroid.y.mean(), centroid.x.mean()]
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# 3. Add the basin polygon to the map
# Styling: fillColor='green', color='darkgreen', fillOpacity=0.2
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

# 4. Coordinates handling
# Context does not provide specific WKT coordinates for the rivers or observation points,
# so no hardcoded list of dictionaries is added here to avoid hallucination.
# If WKT were provided, they would be processed here.

# 5. Save the final map strictly as "133.html"
m.save("133.html")