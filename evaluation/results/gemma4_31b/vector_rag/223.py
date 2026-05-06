import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize the folium map with the specified tiles
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# Add the basin boundary to the map
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

# Context contains entities (Bayankol village), but no WKT coordinates were provided.
# If coordinates were present, they would be added here as a hardcoded list of dictionaries.
# Example structure if coordinates existed:
# observations = [{"name": "Bayankol village 1", "coords": [lat, lon]}, ...]
# for obs in observations:
#     folium.Marker([obs["coords"][0], obs["coords"][1]], popup=obs["name"]).add_to(m)

# Save the final map strictly as 223.html
m.save("223.html")