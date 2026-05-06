import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(gdf.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    gdf,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
# For example:
# sensors = [
#     {"name": "Sensor1", "geometry": wkt.loads("POINT(53.74932 23.82287)")},
#     {"name": "Sensor2", "geometry": wkt.loads("POINT(53.75012 23.82347)")}
# ]

# Add sensors to the map (if available)
# for sensor in sensors:
#     folium.Marker(sensor['geometry'], popup=sensor['name']).add_to(m)

# Save the final map
m.save("71.html")