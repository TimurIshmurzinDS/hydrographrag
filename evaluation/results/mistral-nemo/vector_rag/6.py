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
    {'type': 'FeatureCollection', 'features': [{'geometry': wkt.loads('POINT (-74.0060 4.5703)'), 'properties': {}, 'type': 'Feature'}]}
]

# Add the coordinates to the map
for coord in coordinates:
    folium.GeoJson(coord, style_function=lambda x: {'fillColor': 'blue', 'color': 'blue', 'weight': 2}).add_to(m)

# Save the final map
m.save("6.html")