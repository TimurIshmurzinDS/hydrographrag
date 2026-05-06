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
    data=r'{"type": "FeatureCollection", "features": [{"type": "Polygon", "coordinates": [[[74.5, 43], [76, 42], [78, 41], [80, 40]]]}]}}',
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
coordinates = [
    {"type": "Feature", "geometry": wkt.loads('POINT(76.5 42.5)'), "properties": {"water_level": 10, "date": "2022-01-01"}},
    {"type": "Feature", "geometry": wkt.loads('POINT(78.0 41.0)'), "properties": {"water_level": 15, "date": "2022-02-15"}}
]

# Add the coordinates to the map
for coord in coordinates:
    folium.CircleMarker(
        location=tuple(coord['geometry'].coords[0]),
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)

# Save the final map
m.save("236.html")