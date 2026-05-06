import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# 2. Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 3. Calculate the centroid of the basin to initialize the map
centroid = basin_gdf.geometry.centroid
mean_lat = centroid.y.mean()
mean_lon = centroid.x.mean()

# 4. Initialize folium Map
m = folium.Map(
    location=[mean_lat, mean_lon], 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 5. Add the basin boundary to the map
# Using specified colors and opacity
folium.GeoJson(
    basin_gdf, 
    fillColor='green', 
    color='darkgreen', 
    fillOpacity=0.2
).add_to(m)

# Note: The context provided descriptions of observation points 
# (0.2 km above the confluence with Osek River) but did not provide 
# specific WKT coordinates. If WKT coordinates were provided, 
# they would be added here as a hardcoded list of dictionaries.

# 6. Save the final map strictly as "207.html"
m.save("207.html")