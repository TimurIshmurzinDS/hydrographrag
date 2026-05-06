import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile strictly using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize folium Map using the centroid of the basin shapefile
centroid = basin_gdf.geometry.centroid
map_center = [centroid.y.iloc[0], centroid.x.iloc[0]]

m = folium.Map(
    location=map_center, 
    zoom_start=12, 
    tiles='CartoDB positron'
)

# 3. Add the basin boundary to the map
folium.GeoJson(
    basin_gdf,
    fillColor='green',
    color='darkgreen',
    fillOpacity=0.2,
    popup='Basin Boundary'
).add_to(m)

# 4. Hardcoded list of entities from context 
# (Since no WKT coordinates were provided in the context, 
# we define the entities conceptually for the map if coordinates were available)
entities = [
    {"name": "Tekeli River", "type": "HY_HydroFeature"},
    {"name": "Temirlik River", "type": "HY_HydroFeature"},
    {"name": "Temirlik village", "type": "Observation"}
]

# Note: If WKT coordinates were present in the context, 
# they would be iterated here to add folium.Marker or folium.PolyLine.

# 5. Save the final map strictly as 107.html
m.save("107.html")