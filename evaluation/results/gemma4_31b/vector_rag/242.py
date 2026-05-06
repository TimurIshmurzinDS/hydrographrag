import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize folium Map with the specified tiles
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# Add the basin boundary to the map
# Using specified colors and opacity for the hydrographic basin
folium.GeoJson(
    basin_gdf,
    fillColor='green',
    color='darkgreen',
    fillOpacity=0.2,
    name='Tentek River Basin'
).add_to(m)

# Context contains observation points but no specific WKT coordinates were provided.
# If WKT coordinates were present, they would be added here as a hardcoded list.
# Example structure for future implementation:
# points = [{"loc": [lat, lon], "name": "Observation Point 0.2km above Osek"}]
# for pt in points:
#     folium.Marker([pt["loc"][0], pt["loc"][1]], popup=pt["name"]).add_to(m)

# Save the final map strictly as 242.html
m.save("242.html")