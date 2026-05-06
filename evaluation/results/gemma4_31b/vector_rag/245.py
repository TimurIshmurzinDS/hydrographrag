import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile using a raw string and convert to CRS EPSG:4326
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = gdf.geometry.centroid.iloc[0]
center_lat = centroid.y
center_lon = centroid.x

# Initialize folium Map with the centroid and specific tiles
m = folium.Map(
    location=[center_lat, center_lon], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# Add the basin boundary to the map
# Note: basin_data.shp contains only the exterior polygon boundaries
folium.GeoJson(
    gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# The context does not provide specific WKT coordinates for the observation points,
# so no hardcoded list of dictionaries is added.

# Save the final map strictly as 245.html
m.save("245.html")