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

# Define rivers coordinates in WKT format
rivers = [
    {'name': 'Тентек', 'geom': wkt.loads('POINT(51.4879 -0.3615)')},
    {'name': 'Быж', 'geom': wkt.loads('POINT(52.2345 -0.2345)')}
]

# Add rivers to the map
for river in rivers:
    folium.Marker(location=river['geom'].xy, popup=river['name']).add_to(m)

# Save the final map
m.save("98.html")