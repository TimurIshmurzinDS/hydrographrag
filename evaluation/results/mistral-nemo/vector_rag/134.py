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
    data=r'{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": ' + wkt.loads(str(basin_data.geometry[0])) + ', "properties": {}}]}',
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
river_coords = [
    {"name": "Bayankol River", "wkt": "<WKT_POLYGON_OF_BAYANKOL_RIVER>"},
    {"name": "Kishi Almaty River", "wkt": "<WKT_POLYGON_OF_KISHI_ALMATY_RIVER>"},
]

# Add rivers to the map
for river in river_coords:
    folium.GeoJson(
        data=r'{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": ' + wkt.loads(river["wkt"]) + ', "properties": {}}]}',
        style_function=lambda x: {'fillColor': 'blue', 'color': 'darkblue', 'fillOpacity': 0.2},
    ).add_to(m)

# Save the final map
m.save("134.html")