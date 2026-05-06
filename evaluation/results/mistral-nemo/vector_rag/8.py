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

# Create a hardcoded list of dictionaries for coordinates (WKT)
coordinates = [
    {'type': 'FeatureCollection', 'features': [{'geometry': wkt.loads('POINT(71.45 43.25)'), 'properties': {}}]}
]

# Add the coordinates to the map
folium.GeoJson(coordinates, fillColor='red', color='red', fillOpacity=0.8).add_to(m)

# Save the final map
m.save("8.html")