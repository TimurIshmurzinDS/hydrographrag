import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# 2. Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 3. Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid
center_lat = centroid.y.mean()
center_lon = centroid.x.mean()

# 4. Initialize folium Map
m = folium.Map(
    location=[center_lat, center_lon], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# 5. Add the basin boundary to the map
folium.GeoJson(
    basin_gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    },
    name="Basin Boundary"
).add_to(m)

# 6. Handle coordinates if provided in context (WKT)
# In this specific context, no WKT coordinates were provided for the rivers or the village.
# If they were present, they would be added here as a list of dictionaries.
entities_coords = [] 
for entity in entities_coords:
    folium.Marker(
        location=[entity['lat'], entity['lon']], 
        popup=entity['name']
    ).add_to(m)

# 7. Save the final map strictly as 120.html
m.save("120.html")