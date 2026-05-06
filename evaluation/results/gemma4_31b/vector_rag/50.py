import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize folium.Map using the centroid of the basin shapefile
# Calculate centroid for centering the map
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

m = folium.Map(
    location=map_center, 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 3. Add the basin boundary to the map
# Styling as per strict requirements: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name="Dos River Basin"
).add_to(m)

# 4. Coordinates handling
# Context did not provide specific WKT coordinates for monitoring stations, 
# so no hardcoded list of dictionaries is added here.

# 5. Save the final map strictly as "50.html"
m.save("50.html")