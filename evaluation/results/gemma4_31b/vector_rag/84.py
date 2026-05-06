import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin boundary shapefile
# Using raw string for path as per instructions
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 (EPSG:4326) for folium compatibility
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize the map
# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
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
    },
    name="Basin Boundary"
).add_to(m)

# 4. Handle Coordinates (WKT)
# The context provided entities but no specific WKT strings.
# If WKT coordinates for Observation_2190 were provided, they would be added here.
# Example structure for future implementation:
# points = [
#     {"name": "Observation_2190", "geometry": wkt.loads("POINT(lon lat)")},
# ]
# for pt in points:
#     folium.Marker([pt["geometry"].y, pt["geometry"].x], popup=pt["name"]).add_to(m)

# 5. Save the final map strictly as 84.html
m.save("84.html")