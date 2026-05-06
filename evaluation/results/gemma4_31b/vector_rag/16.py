import geopandas as gpd
import folium
from shapely import wkt

# Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to initialize the map
centroid = basin_gdf.geometry.centroid
mean_lat = centroid.y.mean()
mean_lon = centroid.x.mean()

# Initialize folium Map with the specified tiles
m = folium.Map(location=[mean_lat, mean_lon], tiles='CartoDB positron', zoom_start=12)

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

# The context mentions an observation point "1.1 km above Lake Ulken Almaty", 
# but no WKT coordinates were provided in the context. 
# If coordinates were present, they would be added here as a hardcoded list.

# Save the final map strictly as 16.html
m.save("16.html")