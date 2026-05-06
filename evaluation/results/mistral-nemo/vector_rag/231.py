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
    data=r'{"type": "FeatureCollection", "features": [{"type": "Polygon", "coordinates": [[[74.5, 41.0], [74.5, 39.0], [76.0, 39.0], [76.0, 41.0]]]}]}}',
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
    highlight_function=lambda x: folium.GeoJsonHighlight(style_function).add_to(m)
).add_to(m)

# If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
rivers_data = [
    {'name': 'Коктал', 'wkt': 'POLYGON((...))'},
    {'name': 'Косу', 'wkt': 'POLYGON((...))'},
    {'name': 'Картаал', 'wkt': 'POLYGON((...))'},
    {'name': 'Кумбель', 'wkt': 'POLYGON((...))'},
    {'name': 'Байанкол', 'wkt': 'POLYGON((...))'}
]

# Add rivers to the map
for river in rivers_data:
    folium.GeoJson(
        data=river['wkt'],
        style_function=lambda x: {'fillColor': 'blue', 'color': 'darkblue', 'fillOpacity': 0.2},
        highlight_function=lambda x: folium.GeoJsonHighlight(style_function).add_to(m)
    ).add_to(m)

# Save the final map
m.save("231.html")