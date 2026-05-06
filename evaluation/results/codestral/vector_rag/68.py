import geopandas as gpd
import folium
from shapely import wkt

# Load the basin data
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize folium map with basin centroid
m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries for observations (replace with actual data if available)
observations = [{'name': 'Observation Point', 'coordinates': wkt.loads('POINT (longitude latitude)')}] # Replace longitude and latitude with actual coordinates

# Add observation points to the map
for obs in observations:
    folium.Marker(location=[obs['coordinates'].y, obs['coordinates'].x], popup=obs['name']).add_to(m)

# Save the final map
m.save("68.html")