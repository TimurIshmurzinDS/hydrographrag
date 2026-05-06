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
center_lat = centroid.y.iloc[0]
center_lon = centroid.x.iloc[0]

# 4. Initialize folium Map
# Using 'CartoDB positron' tiles as requested
m = folium.Map(location=[center_lat, center_lon], 
               zoom_start=10, 
               tiles='CartoDB positron')

# 5. Add the basin boundary to the map
# Styling: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name='Prokhodnaya River Basin'
).add_to(m)

# Note: No WKT coordinates were provided in the context for the observation point,
# so no hardcoded point list is added to the map.

# 6. Save the final map strictly as "87.html"
m.save("87.html")