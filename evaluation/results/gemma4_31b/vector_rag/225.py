import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
gdf = gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = gdf.geometry.centroid
center_lat = centroid.y.mean()
center_lon = centroid.x.mean()

# Initialize folium Map with specified tiles
m = folium.Map(
    location=[center_lat, center_lon], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# Add the basin boundary to the map
# Using specified colors: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# Save the final map strictly as 225.html
m.save("225.html")