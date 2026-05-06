import geopandas as gpd
import folium
from shapely import wkt

# a) Load the shapefile and initialize the map
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')
folium.GeoJson(
    basin_data,
    style_function=lambda x, yz, z: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# b) If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
coordinates = [
    {'type': 'FeatureCollection', 'features': [{'geometry': wkt.loads('POINT(74.561983 43.250956)', srs='EPSG:4326'), 'properties': {}}} for _ in range(3)]}
]

# Add coordinates to the map
for coord in coordinates:
    folium.GeoJson(coord).add_to(m)

# Save the final map
m.save("235.html")