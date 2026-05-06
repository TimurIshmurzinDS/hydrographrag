import geopandas as gpd
import folium
from shapely import wkt

# Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_df = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_df = basin_df.to_crs('EPSG:4326')

# Calculate the centroid of the basin to initialize the map center
centroid = basin_df.geometry.centroid
center_lat = centroid.y.iloc[0]
center_lon = centroid.x.iloc[0]

# Initialize folium Map with the specified tiles
m = folium.Map(
    location=[center_lat, center_lon], 
    tiles='CartoDB positron', 
    zoom_start=12
)

# Add the basin boundary to the map with strict styling
folium.GeoJson(
    basin_df, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# Note: No WKT coordinates were provided in the context for the Observation entities,
# therefore no hardcoded point markers are added to the map.

# Save the final map strictly as 8.html
m.save("8.html")