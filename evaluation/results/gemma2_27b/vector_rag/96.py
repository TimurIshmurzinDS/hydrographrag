import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize map centered on basin centroid
m = folium.Map(location=basin.centroid.values[0], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(data=basin, name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Define hardcoded list of dictionaries with coordinates (WKT)
coordinates = [
    {'name': 'Urzhar River', 'wkt': 'POINT (61.5432 78.9876)'},  
    {'name': 'Dos River', 'wkt': 'POINT (61.5432 78.9876)'}
]

# Add markers for each point to the map
for coord in coordinates:
    folium.Marker(location=wkt.loads(coord['wkt']).coords[0], popup=coord['name'], tooltip=coord['name']).add_to(m)

# Save the map
m.save("96.html")