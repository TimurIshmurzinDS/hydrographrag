import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
# For example:
# sensors = [
#     {'type': 'Feature', 'geometry': wkt.loads('POINT(74.56 43.25)'), 'properties': {'name': 'Sensor 1'}},
#     {'type': 'Feature', 'geometry': wkt.loads('POINT(74.89 43.12)'), 'properties': {'name': 'Sensor 2'}}
# ]

# Add sensors to the map using folium.Marker
# for sensor in sensors:
#     folium.Marker(sensor['geometry'], popup=sensor['properties']['name']).add_to(m)

# Save the final map
m.save("144.html")