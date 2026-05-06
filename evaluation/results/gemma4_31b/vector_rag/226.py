import geopandas as gpd
import folium
from shapely import wkt

# Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to initialize the map center
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize folium Map with specified tiles
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# Add the basin boundary to the map
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# The context mentions 'Dobyn pier' as an Observation entity, 
# but no WKT coordinates were provided in the input context.
# If coordinates were present, they would be added here as a hardcoded list.

# Save the final map strictly as 226.html
m.save("226.html")