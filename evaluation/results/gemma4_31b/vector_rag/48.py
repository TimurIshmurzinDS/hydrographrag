import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin boundary shapefile using a raw string
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
# Using specified colors and opacity
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# Note: No WKT coordinates were provided in the context for specific river points.
# If coordinates were available, they would be added here as a hardcoded list of dictionaries.

# 6. Save the final map strictly as "48.html"
m.save("48.html")