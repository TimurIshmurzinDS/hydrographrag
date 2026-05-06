import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# 2. Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 3. Calculate the centroid of the basin to initialize the map
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# 4. Initialize folium Map
# Using 'CartoDB positron' tiles as requested
m = folium.Map(location=map_center, zoom_start=10, tiles='CartoDB positron')

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
    name='Sarykan River Basin'
).add_to(m)

# 6. Handle Coordinates (WKT) if they were provided in context
# Since no specific WKT coordinates were provided in the context for points, 
# we skip the hardcoded list of dictionaries to avoid adding empty data.
# If coordinates were present, they would be added here as folium.Marker.

# 7. Save the final map strictly as "52.html"
m.save("52.html")