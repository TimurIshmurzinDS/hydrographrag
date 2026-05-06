import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_df = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 CRS
basin_df = basin_df.to_crs('EPSG:4326')

# Calculate the centroid of the basin for map initialization
centroid = basin_df.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize folium Map
m = folium.Map(location=map_center, zoom_start=12, tiles='CartoDB positron')

# Add the basin boundary to the map
folium.GeoJson(
    basin_df,
    name="Kishi Almaty River Basin",
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# The context mentions an observation point 1.1 km above Lake Ulken Almaty, 
# but no specific WKT coordinates were provided in the input.
# If coordinates were present, they would be added here as a hardcoded list.

# Save the final map strictly as 217.html
m.save("217.html")