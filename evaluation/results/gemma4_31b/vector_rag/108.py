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

# 4. Initialize folium Map with specified tiles
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

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
    name="Basin Boundary"
).add_to(m)

# 6. Handle coordinates for the rivers
# Since no WKT coordinates were provided in the context, 
# we define the entities as a list for potential future mapping.
river_entities = [
    {"name": "Kurty River", "type": "HY_HydroFeature"},
    {"name": "Urzhar River", "type": "HY_HydroFeature"},
    {"name": "Uzyn Kargaly River", "type": "HY_HydroFeature"},
    {"name": "Shyzhyn River", "type": "HY_HydroFeature"},
    {"name": "Byzhy River", "type": "HY_HydroFeature"}
]

# Note: If WKT coordinates were present, they would be iterated here 
# and added as folium.Marker or folium.PolyLine.

# 7. Save the final map strictly as 108.html
m.save("108.html")