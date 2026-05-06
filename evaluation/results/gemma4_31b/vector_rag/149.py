import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize the map
# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid
center_lat = centroid.y.mean()
center_lon = centroid.x.mean()

m = folium.Map(
    location=[center_lat, center_lon], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# 3. Add the basin boundary to the map
folium.GeoJson(
    basin_gdf, 
    fillColor='green', 
    color='darkgreen', 
    fillOpacity=0.2
).add_to(m)

# 4. Handle sensor coordinates
# Context provided entities (Observation_0, Observation_1, Observation_2264) 
# but no WKT coordinates were explicitly provided in the context.
# If coordinates were present, they would be added here as a hardcoded list.
sensors_data = [] 

for sensor in sensors_data:
    folium.Marker(
        location=[sensor['lat'], sensor['lon']], 
        popup=sensor['name']
    ).add_to(m)

# 5. Save the final map strictly as 149.html
m.save("149.html")