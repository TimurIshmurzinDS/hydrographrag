import geopandas as gpd
import folium
from shapely import wkt

# Load the basin data
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium map with basin centroid
m = folium.Map(location=[basin_data['geometry'].centroid.y, basin_data['geometry'].centroid.x], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries for observation points (replace with actual data if available)
observation_points = [{'name': 'Observation Point', 'coordinates': wkt.loads('POINT (37.6184 55.7512)'}]} # Replace coordinates with actual data

# Add observation points to the map
for point in observation_points:
    folium.Marker(location=[point['coordinates'].y, point['coordinates'].x], popup=point['name']).add_to(m)

# Save the final map
m.save("19.html")