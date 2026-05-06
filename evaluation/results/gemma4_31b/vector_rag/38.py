import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# 2. Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 3. Calculate the centroid of the basin to initialize the map
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# 4. Initialize folium Map
m = folium.Map(
    location=map_center, 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 5. Add the basin boundary to the map
folium.GeoJson(
    basin_gdf, 
    fillColor='green', 
    color='darkgreen', 
    fillOpacity=0.2
).add_to(m)

# 6. Hardcoded coordinates for entities if WKT were provided in context.
# Since no WKT coordinates were provided in the context, this list remains empty.
# Example structure: points = [{"name": "Karkara Obs Point", "coords": [lat, lon]}]
points = []

for point in points:
    folium.Marker(
        location=[point["coords"][0], point["coords"][1]], 
        popup=point["name"]
    ).add_to(m)

# 7. Save the final map strictly as 38.html
m.save("38.html")