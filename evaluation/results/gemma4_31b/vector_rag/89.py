import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile strictly using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize folium Map
# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid
center_lat = centroid.y.iloc[0]
center_lon = centroid.x.iloc[0]

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

# 4. Handle Entities (Coordinates are not provided in WKT in context, 
# but we define the logic for the identified observation points)
# If WKT coordinates were present, they would be added here as a list of dicts.
entities = [
    {"name": "Baskan River", "type": "HY_HydroFeature"},
    {"name": "Prokhodnaya River", "type": "HY_HydroFeature"},
    {"name": "Observation Point (2km above mouth of Prokhodnaya)", "type": "Observation"}
]

# Note: Since no specific WKT coordinates were provided in the context, 
# we cannot plot specific points, but the basin is rendered.

# 5. Save the final map strictly as "89.html"
m.save("89.html")