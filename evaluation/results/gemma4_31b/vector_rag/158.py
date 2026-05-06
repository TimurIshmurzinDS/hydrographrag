import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_df = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_df = basin_df.to_crs('EPSG:4326')

# 2. Initialize the map using the centroid of the basin polygon
centroid = basin_df.geometry.centroid
map_center = [centroid.y.iloc[0], centroid.x.iloc[0]]

m = folium.Map(
    location=map_center, 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 3. Add the basin boundary to the map
folium.GeoJson(
    basin_df,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name="Basin Boundary"
).add_to(m)

# 4. Hardcoded entities from context (Coordinates not provided in WKT, 
# but structure is maintained for potential additions)
# Since no WKT coordinates were provided in the context, we focus on the basin.
# If coordinates were present, they would be added here as folium.Marker.

# 5. Save the final map strictly as 158.html
m.save("158.html")