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

# Hardcoded list of dictionaries containing coordinates (WKT) for Bayankol River and Bayankol village
coordinates = [
    {'type': 'FeatureCollection', 'features': [{'geometry': wkt.loads('POINT(74.95 43.18)'), 'properties': {}, 'type': 'Feature'}, {'geometry': wkt.loads('POLYGON((74.90 43.20, 74.95 43.18, 75.00 43.16, 75.05 43.14, 75.10 43.12, 75.15 43.10, 75.20 43.08, 75.25 43.06, 75.30 43.04, 75.35 43.02, 75.40 43.00))'), 'properties': {}, 'type': 'Feature'}]}
]

# Add Bayankol River and Bayankol village to the map
for coord in coordinates:
    folium.GeoJson(coord).add_to(m)

# Save the final map
m.save("257.html")