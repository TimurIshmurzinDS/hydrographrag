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
    name="Basin Boundary"
).add_to(m)

# 6. Handle coordinates from context
# Context mentions: Aksu River, Lepsy River, Koksu River, аул Lepsy.
# No WKT coordinates were provided in the context, so we skip hardcoded points.
# If WKT were present, they would be added here as folium.Marker.

# 7. Save the final map strictly as "201.html"
m.save("201.html")