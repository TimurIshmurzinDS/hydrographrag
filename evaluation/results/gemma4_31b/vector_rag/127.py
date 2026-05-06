import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile
# Using raw string for path as per instructions
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326'
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize folium Map
# Calculate centroid of the basin for map centering
centroid = basin_gdf.geometry.centroid
center_lat = centroid.y.mean()
center_lon = centroid.x.mean()

m = folium.Map(
    location=[center_lat, center_lon], 
    tiles='CartoDB positron', 
    zoom_start=6
)

# 3. Add the basin boundary to the map
folium.GeoJson(
    basin_gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# 4. Handle Coordinates (WKT)
# The context provided does not contain specific WKT coordinates for the river or stations.
# If they were present, they would be added here as a hardcoded list of dictionaries.
coordinates_list = [] 
for coord in coordinates_list:
    # Example of how points would be added if coordinates existed:
    # folium.Marker([coord['lat'], coord['lon']], popup=coord['name']).add_to(m)
    pass

# 5. Save the final map
m.save("127.html")