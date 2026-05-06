import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# 2. Convert to CRS 'EPSG:4326' for web mapping
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 3. Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# 4. Initialize folium Map with CartoDB positron tiles
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=12)

# 5. Add the basin boundary to the map with specific styling
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# 6. Coordinates for sensors (WKT not provided in context, 
# but structure is ready for hardcoded list if coordinates were present)
# Example: sensors = [{"name": "Sensor 1", "coords": [lat, lon]}]
# Since no WKT is provided, we proceed to save the basin map.

# 7. Save the final map strictly as "73.html"
m.save("73.html")