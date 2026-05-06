import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium map using the centroid of the shapefile
m = folium.Map(location=[basin_data['geometry'].centroid.y.mean(), basin_data['geometry'].centroid.x.mean()], tiles='CartoDB positron')

# Add the basins to the map
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries for observation points in аул Lepsy (replace with actual data if available)
observation_points = [{'name': 'Observation Point 1', 'coordinates': wkt.loads('POINT (60.52401 72.39875)'},
                      {'name': 'Observation Point 2', 'coordinates': wkt.loads('POINT (60.52502 72.39976)'},
                      # Add more observation points as needed
                     ]

# Add the observation points to the map
for point in observation_points:
    folium.Marker(location=[point['coordinates'].y, point['coordinates'].x], popup=point['name']).add_to(m)

# Save the final map
m.save("198.html")