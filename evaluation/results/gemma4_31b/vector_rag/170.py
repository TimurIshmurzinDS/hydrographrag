import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_path = r"data/basin_data.shp"
basin_df = gpd.read_file(basin_path)

# Convert to WGS84 CRS for folium compatibility
basin_df = basin_df.to_crs('EPSG:4326')

# 2. Calculate the centroid of the basin to center the map
centroid = basin_df.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# 3. Initialize folium Map with specified tiles
m = folium.Map(
    location=map_center, 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 4. Add the basin boundary to the map
# Styling: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    basin_df,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name="Water Basin Boundary"
).add_to(m)

# Note: Coordinates for Terisbuthak Creek were not provided in the context WKT.
# If coordinates were present, they would be added here as folium.Marker.

# 5. Save the final map strictly as 170.html
m.save("170.html")