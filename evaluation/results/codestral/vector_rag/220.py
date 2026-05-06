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

# Hardcoded list of dictionaries for observation points (replace with actual data if available)
observation_points = [{'name': 'Observation Point 1', 'coordinates': wkt.loads('POINT (37.6200 55.7540)'},
                      {'name': 'Observation Point 2', 'coordinates': wkt.loads('POINT (37.6220 55.7560)'}
                     ]

# Add observation points to the map
for point in observation_points:
    folium.Marker(location=[point['coordinates'].y, point['coordinates'].x], popup=point['name']).add_to(m)

# Save the final map
m.save("220.html")