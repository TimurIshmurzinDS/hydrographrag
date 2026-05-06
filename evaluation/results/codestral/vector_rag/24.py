import geopandas as gpd
import folium
from shapely import wkt

# Load the basin data
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium map with basin centroid
m = folium.Map(location=[basin_data['geometry'].centroid.y.mean(), basin_data['geometry'].centroid.x.mean()], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries with coordinates from the context
observations = [{'name': '1.1 km above Lake Ulken Almaty', 'coordinates': wkt.loads('POINT (78.3945 42.6026)')}]

# Add observations to the map
for observation in observations:
    folium.Marker(location=[observation['coordinates'].y, observation['coordinates'].x], popup=observation['name']).add_to(m)

# Save the final map
m.save("24.html")