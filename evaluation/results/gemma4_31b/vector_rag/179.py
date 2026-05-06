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
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=12)

# Add the basin boundary to the map
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name='Basin Boundary'
).add_to(m)

# The context does not provide specific WKT coordinates for the river or observation point.
# If coordinates were provided, they would be added here as a list of dictionaries.
# Example structure for future implementation:
# points_to_plot = [{"name": "Observation Point", "coords": [lat, lon]}]
# for pt in points_to_plot:
#     folium.Marker([pt["coords"][0], pt["coords"][1]], popup=pt["name"]).add_to(m)

# Save the final map strictly as 179.html
m.save("179.html")