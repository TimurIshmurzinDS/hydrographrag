import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize the map using the centroid of the basin
centroid = basin_gdf.geometry.centroid
map_center = [centroid.y.iloc[0], centroid.x.iloc[0]]

m = folium.Map(
    location=map_center, 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 3. Add the basin boundary to the map
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# 4. Handle coordinates from context
# Note: The context provided descriptions but no WKT coordinates.
# If WKT coordinates were present, they would be added here as a hardcoded list.
observations = [] 
# Example structure if coordinates existed:
# observations = [{"name": "Sensor 1", "geometry": wkt.loads("POINT(lon lat)")}]

for obs in observations:
    coords = [obs["geometry"].y, obs["geometry"].x]
    folium.Marker(
        location=coords,
        popup=obs["name"],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 5. Save the final map strictly as 12.html
m.save("12.html")