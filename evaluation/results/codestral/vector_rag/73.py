import geopandas as gpd
import folium
from shapely import wkt

# Load the basin data
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize folium map with basin centroid
m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin['geometry'], style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries for river features and observation point
features = [{'name': 'Koktal River', 'type': 'HY_HydroFeature'}, {'name': 'Osek River', 'type': 'HY_HydroFeature'}, {'name': 'Observation Point', 'type': 'Observation'}]

# Assuming we have coordinates for the observation point, add it to the map
observation_point = wkt.loads('POINT (longitude latitude)')  # Replace longitude and latitude with actual values
folium.Marker(location=[observation_point.y, observation_point.x], popup='0.2 km above confluence with Osek River').add_to(m)

# Save the final map
m.save("73.html")