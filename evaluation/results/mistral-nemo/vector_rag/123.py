import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add basin to the map
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If context contains Coordinates (WKT), create a hardcoded list of dictionaries
coordinates = [
    {'name': 'Kurty River', 'wkt': 'POINT(75.1234 45.6789)'},
    {'name': 'Sharyn River', 'wkt': 'POINT(76.2345 46.7890)'}
]

# Add rivers to the map
for river in coordinates:
    folium.Marker(location=wkt.loads(river['wkt']), popup=river['name']).add_to(m)

# Save the final map
m.save("123.html")