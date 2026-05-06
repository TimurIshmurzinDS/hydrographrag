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
    data=r'{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": ' + basin_data.to_json() + r'}, {"properties": {}, "geometry": {' + basin_data.geometry.to_wkt() + r"}}}}]}',
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
coordinates = [
    {"type": "Feature", "geometry": wkt.loads('POINT (-71.83 40.59)'), "properties": {"name": "Sarykan River"}},
    {"type": "Feature", "geometry": wkt.loads('POINT (-72.67 41.12)'), "properties": {"name": "Aksu River"}}
]

# Add the coordinates to the map
for coord in coordinates:
    folium.Marker(location=tuple(coord['geometry'].coords[0]), popup=coord['properties']['name']).add_to(m)

# Save the final map
m.save("106.html")