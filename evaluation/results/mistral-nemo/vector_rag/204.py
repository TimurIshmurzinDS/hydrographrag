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
    data=r'{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": ' + wkt.loads(basin_data['geometry'].iloc[0]).wkt + ', "properties": {}}]}',
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
    highlight_function=lambda x: {'weight': 2}
).add_to(m)

# If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
byzhy_river = {"type": "Feature", "geometry": wkt.loads('POINT(51.4370 -0.649)'), "properties": {}}
urzhar_river = {"type": "Feature", "geometry": wkt.loads('POINT(52.2830 0.139)'), "properties": {}}

# Add rivers to the map
folium.GeoJson(byzhy_river, style_function=lambda x: {'color': 'blue', 'weight': 2}).add_to(m)
folium.GeoJson(urzhar_river, style_function=lambda x: {'color': 'red', 'weight': 2}).add_to(m)

# Save the final map
m.save("204.html")