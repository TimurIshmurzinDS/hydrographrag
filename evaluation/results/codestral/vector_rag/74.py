import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=[basin_data.centroid.y.mean(), basin_data.centroid.x.mean()], tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Create a hardcoded list of dictionaries for the observation points (replace with actual coordinates if available)
observation_points = [{'name': 'Observation Point 1', 'coordinates': wkt.loads('POINT (37.6200 55.7540)'},
                      {'name': 'Observation Point 2', 'coordinates': wkt.loads('POINT (37.6220 55.7520)'}
                     ]

# Add the observation points to the map
for point in observation_points:
    folium.Marker(location=[point['coordinates'].y, point['coordinates'].x], popup=point['name']).add_to(m)

# Save the final map
m.save("74.html")