import geopandas as gpd
import folium
from shapely import wkt

# Load the basin shapefile using a raw string
basin_df = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326'
basin_df = basin_df.to_crs('EPSG:4326')

# Calculate the centroid of the basin for map initialization
centroid = basin_df.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize folium Map
m = folium.Map(location=map_center, zoom_start=10, tiles='CartoDB positron')

# Add the basin boundary to the map
folium.GeoJson(
    basin_df,
    fillColor='green',
    color='darkgreen',
    fillOpacity=0.2,
    popup='Basin Boundary'
).add_to(m)

# The context provided entity IDs but no WKT coordinates. 
# If coordinates were provided, they would be added here as a hardcoded list.
# Example structure if WKT existed:
# observations = [
#     {"id": "Observation_2190", "geometry": wkt.loads("POINT(x y)")},
#     ...
# ]
# for obs in observations:
#     folium.Marker([obs["geometry"].y, obs["geometry"].x], popup=obs["id"]).add_to(m)

# Save the final map strictly as 274.html
m.save("274.html")