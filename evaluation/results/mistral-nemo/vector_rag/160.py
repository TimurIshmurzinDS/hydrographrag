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
    data=basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If we had coordinates (WKT) for Ili River and Shyzhyn River, we could create a hardcoded list of dictionaries like this:
# ili_river = {'type': 'Feature', 'geometry': wkt.loads('POINT(74.56 43.29)'), 'properties': {'name': 'Ili River'}}
# shyzhyn_river = {'type': 'Feature', 'geometry': wkt.loads('POINT(70.18 49.83)'), 'properties': {'name': 'Shyzhyn River'}}

# If we had these coordinates, we could add them to the map like this:
# folium.GeoJson(
#     data=[ili_river, shyzhyn_river],
#     style_function=lambda x: {'fillColor': 'blue', 'color': 'blue', 'fillOpacity': 0.5},
# ).add_to(m)

# Save the final map
m.save("160.html")