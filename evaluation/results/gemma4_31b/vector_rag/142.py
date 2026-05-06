import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile
# Using raw string for path as per instructions
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin for map initialization
centroid = basin_gdf.geometry.centroid
mean_lat = centroid.y.mean()
mean_lon = centroid.x.mean()

# Initialize folium map with specified tiles
m = folium.Map(
    location=[mean_lat, mean_lon], 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# Add the basin boundary to the map with strict styling
folium.GeoJson(
    basin_gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# The context provides relative location (1.7 km above mouth) but no WKT coordinates.
# If WKT coordinates were provided, they would be added here as a hardcoded list.
monitoring_points = [] 

for point in monitoring_points:
    folium.Marker(
        location=[point['lat'], point['lon']], 
        popup=point['name']
    ).add_to(m)

# Save the final map strictly as 142.html
m.save("142.html")