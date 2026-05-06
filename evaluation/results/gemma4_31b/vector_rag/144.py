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
map_center = [centroid.y.iloc[0], centroid.x.iloc[0]]

m = folium.Map(
    location=map_center, 
    tiles='CartoDB positron', 
    zoom_start=6
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
    tooltip="Basin of Ili River"
).add_to(m)

# 4. Coordinates handling
# Since no specific WKT coordinates for sensors were provided in the context, 
# we focus on the basin boundary visualization. 
# If coordinates were present, they would be added here as a hardcoded list of dictionaries.

# 5. Save the final map strictly using the required filename
m.save("144.html")