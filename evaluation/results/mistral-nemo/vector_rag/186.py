import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = "EPSG:4326"

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
coordinates = [
    {'type': 'Point', 'coordinates': [51.5074, -0.1278]},  # Example coordinate for Butak River
    {'type': 'Polygon', 'coordinates': [[[51.51, -0.13], [51.52, -0.13], [51.52, -0.14], [51.51, -0.14]]]}  # Example coordinate for Butak village
]

# Add coordinates to the map
for coord in coordinates:
    folium.GeoJson(coord).add_to(m)

# Save the final map
m.save("186.html")