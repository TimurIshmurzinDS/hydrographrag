import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the shapefile strictly using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize folium.Map using the centroid of the shapefile
# Calculate centroid for centering the map
centroid = basin_gdf.geometry.centroid
center_lat = centroid.y.iloc[0]
center_lon = centroid.x.iloc[0]

m = folium.Map(
    location=[center_lat, center_lon], 
    tiles='CartoDB positron', 
    zoom_start=6
)

# 3. Add the basin boundary to the map
folium.GeoJson(
    basin_gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# Note: No WKT coordinates were provided in the context for specific points, 
# so no hardcoded point list is added.

# 4. Save the final map strictly using the required filename
m.save("39.html")