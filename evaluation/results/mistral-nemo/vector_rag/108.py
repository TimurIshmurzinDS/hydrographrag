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

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
coordinates = [
    {'name': 'Kurty River', 'wkt': 'POINT(51.43 76.89)'},
    {'name': 'Urzhar River', 'wkt': 'POINT(52.12 77.05)'}
]

# Add rivers to the map
for river in coordinates:
    folium.Marker(wkt.loads(river['wkt']), popup=river['name']).add_to(m)

# Save the final map
m.save("108.html")