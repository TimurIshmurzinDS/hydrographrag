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
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=6)

# 5. Add the basin boundary to the map with strict styling
folium.GeoJson(
    basin_gdf,
    fillColor='green',
    color='darkgreen',
    fillOpacity=0.2
).add_to(m)

# 6. Handle coordinates if WKT were present in context
# Since no WKT coordinates were provided in the context, 
# we skip the hardcoded list of dictionaries to avoid dummy data.
# If coordinates were provided, they would be added as folium.Marker here.

# 7. Save the final map strictly as "141.html"
m.save("141.html")