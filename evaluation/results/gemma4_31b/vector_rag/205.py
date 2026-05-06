import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize the map
# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid
center_lat = centroid.y.mean()
center_lon = centroid.x.mean()

m = folium.Map(
    location=[center_lat, center_lon], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# 3. Add the basin boundary to the map
# Using specified colors and opacity
folium.GeoJson(
    basin_gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# 4. Handle coordinates from context
# Context mentions 'аул Lepsy' as Observation, but no WKT coordinates provided.
# If WKT were present, they would be added here as a hardcoded list of dictionaries.
# Example structure (commented out):
# observations = [
#     {"name": "аул Lepsy", "geometry": wkt.loads("POINT(lon lat)")}
# ]
# for obs in observations:
#     folium.Marker([obs['geometry'].y, obs['geometry'].x], popup=obs['name']).add_to(m)

# 5. Save the final map strictly as 205.html
m.save("205.html")