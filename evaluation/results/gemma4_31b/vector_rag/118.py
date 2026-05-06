import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize the folium map
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
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name="Basin Boundary"
).add_to(m)

# 4. Handle entities from context
# Since no WKT coordinates were provided in the context, 
# we define the entities conceptually. If WKT were present, 
# they would be added as folium.Marker or folium.PolyLine.
entities = [
    {"name": "Sarykan River", "type": "HY_HydroFeature"},
    {"name": "Temirlik River", "type": "HY_HydroFeature"},
    {"name": "Temirlik village", "type": "Observation"}
]

# Note: In a real scenario with WKT, we would iterate through a list of 
# coordinates and add them to the map here.

# 5. Save the final map strictly as 118.html
m.save("118.html")