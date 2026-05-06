import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If coordinates (WKT) are provided in the context, create a hardcoded list of dictionaries
coordinates = [
    {'type': 'FeatureCollection', 'features': [{'geometry': wkt.loads('POINT(123.456 78.901)'), 'type': 'Feature', 'properties': {}}]}
]

# Add coordinates to the map
for coord in coordinates:
    folium.GeoJson(coord).add_to(m)

# Save the final map
m.save("268.html")