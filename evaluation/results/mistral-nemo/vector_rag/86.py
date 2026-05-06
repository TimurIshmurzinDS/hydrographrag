import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
coordinates = [
    {'name': 'Темерлик River', 'wkt': 'POINT(51.48 37.65)'},
    {'name': 'Турген River', 'wkt': 'POINT(52.34 38.12)'},
    {'name': 'Караой River', 'wkt': 'POINT(50.98 37.23)'}
]

# Add points to the map
for coord in coordinates:
    folium.Marker(wkt.loads(coord['wkt']), popup=coord['name']).add_to(m)

# Save the final map
m.save("86.html")