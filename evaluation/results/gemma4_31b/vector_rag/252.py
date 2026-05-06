import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the shapefile using a raw string and convert to CRS 'EPSG:4326'
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize folium.Map using the centroid of the basin shapefile
# Using 'CartoDB positron' tiles as requested
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 3. Add the basin boundary to the map
# Styling: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    basin_gdf, 
    fillColor='green', 
    color='darkgreen', 
    fillOpacity=0.2
).add_to(m)

# 4. Coordinates handling
# The context provided properties but no specific WKT coordinates.
# If WKT coordinates were provided, they would be added here as a list of dictionaries.
# Example structure (commented out as no WKT provided in context):
# points = [{"loc": [lat, lon], "name": "Station 1"}]
# for p in points:
#     folium.Marker([p["loc"][0], p["loc"][1]], popup=p["name"]).add_to(m)

# 5. Save the final map strictly as "252.html"
m.save("252.html")