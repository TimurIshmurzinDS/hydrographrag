import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin boundary shapefile
# Using raw string for path as per instructions
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# 2. Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 3. Calculate the centroid of the basin to initialize the map
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# 4. Initialize folium Map
# Using 'CartoDB positron' tiles as required
m = folium.Map(location=map_center, zoom_start=10, tiles='CartoDB positron')

# 5. Add the basin boundary to the map
# Strict styling: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name="Urzhar River Basin"
).add_to(m)

# 6. Hardcoded entities from context (Observation points and Rivers)
# Since WKT coordinates were not provided in the context, 
# we represent the logical presence of these entities.
# In a real scenario, these would be added as folium.Marker or folium.PolyLine.
entities = [
    {"name": "Urzhar River", "type": "HY_HydroFeature"},
    {"name": "Shyzhyn River", "type": "HY_HydroFeature"},
    {"name": "Observation_2264", "type": "Observation"},
    {"name": "Observation_2247", "type": "Observation"},
    {"name": "Observation_2265", "type": "Observation"},
]

# Note: Points are not read from basin_data.shp to avoid FATAL ERROR 1.

# 7. Save the final map strictly as "209.html"
m.save("209.html")