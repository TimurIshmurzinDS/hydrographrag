import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the shapefile using a raw string and convert to CRS 'EPSG:4326'
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# 3. Initialize folium Map with specified tiles
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# 4. Add the basin boundary to the map with strict styling
folium.GeoJson(
    basin_gdf,
    fillColor='green',
    color='darkgreen',
    fillOpacity=0.2
).add_to(m)

# 5. Coordinates (WKT) are not provided in the context, 
# so no hardcoded point list is added.

# 6. Save the final map strictly as "7.html"
m.save("7.html")