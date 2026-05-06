import geopandas as gpd
import folium
from shapely import wkt

# Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to initialize the map center
centroid = basin_gdf.geometry.centroid
mean_lat = centroid.y.mean()
mean_lon = centroid.x.mean()

# Initialize folium Map with the specified tiles
m = folium.Map(location=[mean_lat, mean_lon], tiles='CartoDB positron', zoom_start=10)

# Add the basin boundary to the map
# Using specified colors: fillColor='green', color='darkgreen', fillOpacity=0.2
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

# The context mentions an observation point 1.7 km above the mouth, 
# but no specific WKT coordinates were provided in the input.
# If coordinates were provided, they would be added here as a hardcoded list.

# Save the final map strictly as 184.html
m.save("184.html")