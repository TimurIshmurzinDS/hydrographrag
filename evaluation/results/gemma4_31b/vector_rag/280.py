import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the shapefile using a raw string and convert to CRS EPSG:4326
# The file contains only the exterior polygon boundaries of the basin
basin_df = gpd.read_file(r"data/basin_data.shp")
basin_df = basin_df.to_crs('EPSG:4326')

# 2. Calculate the centroid of the basin to initialize the map
centroid = basin_df.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# 3. Initialize folium Map with the specified tiles
m = folium.Map(location=map_center, zoom_start=8, tiles='CartoDB positron')

# 4. Add the basin boundary to the map
# Strictly using the specified colors and opacity
folium.GeoJson(
    basin_df,
    fillColor='green',
    color='darkgreen',
    fillOpacity=0.2,
    name='Basin Boundary'
).add_to(m)

# 5. Coordinates (WKT) check: 
# No WKT coordinates were provided in the context, so no hardcoded points are added.

# 6. Save the final map strictly as "280.html"
m.save("280.html")