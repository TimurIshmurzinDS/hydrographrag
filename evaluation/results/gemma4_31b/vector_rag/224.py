import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to initialize the map
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize folium map with specified tiles
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# Add the basin boundary to the map with strict styling
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# Context contains entities: Karaoy River, Kurty River, Karatal River.
# No WKT coordinates were provided in the context, so hardcoded list is empty.
# If coordinates were provided, they would be added here as folium.Marker.
river_points = [] 

for point in river_points:
    folium.Marker(
        location=[point['lat'], point['lon']],
        popup=point['name']
    ).add_to(m)

# Save the final map strictly as 224.html
m.save("224.html")