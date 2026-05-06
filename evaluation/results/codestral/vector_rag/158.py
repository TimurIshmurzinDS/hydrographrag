import geopandas as gpd
import folium
from shapely import wkt

# Load the basin data
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize folium map
m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron', zoom_start=10)

# Add the basin to the map
folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries for rivers and village coordinates (WKT format)
# This data should be replaced with real data in a practical scenario
coordinates = [
    {'name': 'Bayankol River', 'type': 'HY_HydroFeature', 'wkt': 'POINT(69.28571 42.03333)'},
    {'name': 'Sarykan River', 'type': 'HY_HydroFeature', 'wkt': 'POINT(70.28571 41.03333)'},
    {'name': 'Bayankol village', 'type': 'Observation', 'wkt': 'POINT(69.58571 41.53333)'}
]

# Add rivers and village to the map
for coord in coordinates:
    folium.Marker([wkt.loads(coord['wkt']).y, wkt.loads(coord['wkt']).x], popup=coord['name'], icon=folium.Icon(color='blue')).add_to(m)

# Save the final map
m.save("158.html")