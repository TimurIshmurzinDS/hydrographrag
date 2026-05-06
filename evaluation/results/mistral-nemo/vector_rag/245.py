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
    data=r'{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": ' + basin_data.to_json() + r'}, {"properties": {}, "id": "basin"}]}}',
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
    highlight_function=lambda x: {'weight': 3}
).add_to(m)

# If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
coordinates = [
    {"type": "Feature", "geometry": wkt.loads('POINT(16.547928 -99.099432)'), "properties": {}},
]

# Add coordinates to the map
for coord in coordinates:
    folium.GeoJson(
        data=r'{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": ' + wkt.dumps(coord['geometry']) + r'}, {"properties": {}, "id": "coord"}]}}',
        style_function=lambda x: {'color': 'red', 'weight': 2},
    ).add_to(m)

# Save the final map
m.save("245.html")