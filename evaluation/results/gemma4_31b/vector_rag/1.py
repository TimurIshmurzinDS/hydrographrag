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
center_lat = centroid.y.mean()
center_lon = centroid.x.mean()

# 4. Initialize folium Map with specified tiles
m = folium.Map(
    location=[center_lat, center_lon], 
    tiles='CartoDB positron', 
    zoom_start=6
)

# 5. Add the basin boundary to the map
# Using specified colors: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    basin_gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# 6. Coordinates for observation points (if WKT were provided in context)
# Since no WKT coordinates were provided in the context, this list remains empty
# but the structure is kept for professional compliance.
observations = [] 
for obs in observations:
    folium.Marker(
        location=[obs['lat'], obs['lon']], 
        popup=obs['name']
    ).add_to(m)

# 7. Save the final map strictly as "1.html"
m.save("1.html")