import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = "EPSG:4326"

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Define coordinates for Koksu River and Byzhy River (hardcoded)
rivers_coords = [
    {"name": "Коксу", "wkt": "POINT(71.5439 -48.6167)"},
    {"name": "Быжы", "wkt": "POINT(72.0167 -48.4167)"}
]

# Create a list of rivers' geometries using wkt.loads()
rivers_geoms = [wkt.loads(coord['wkt']) for coord in rivers_coords]

# Add rivers to the map
for river in rivers_geoms:
    folium.GeoJson(river, style_function=lambda x: {'fillColor': 'blue', 'color': 'blue', 'fillOpacity': 0.5}).add_to(m)

# Save the final map
m.save("208.html")