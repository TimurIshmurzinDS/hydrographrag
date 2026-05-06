import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=[basin.centroid.y[0], basin.centroid.x[0]], tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson
folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
observation_point = wkt.loads('POINT (37.618423 55.751244)') # Replace with actual coordinates from the context
folium.Marker(location=[observation_point.y, observation_point.x], popup='Observation Point').add_to(m)

# Save the final map
m.save("238.html")