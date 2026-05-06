import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# Define coordinates for Dos and Emeel rivers (hardcoded)
dos_river = {"type": "Point", "coordinates": [51.5074, -0.1278]}
emeel_river = {"type": "Point", "coordinates": [52.2370, 6.8205]}

# Calculate distance between Dos and Emeel rivers
dos_point = wkt.loads(dos_river['type'] + '(' + ','.join(map(str, dos_river['coordinates'])) + ')')
emeel_point = wkt.loads(emeel_river['type'] + '(' + ','.join(map(str, emeel_river['coordinates'])) + ')')
distance = dos_point.distance(emeel_point)

# Save the final map
m.save("92.html")