import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=[gdf.centroid.y, gdf.centroid.x], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(gdf.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# If there were coordinates (WKT) in the context, we would create a hardcoded list of dictionaries like this:
# sensors = [
#     {"name": "Koktal River Sensor", "wkt": "POINT(123.456 789.012)", "status": "active"},
#     {"name": "Aksu River Sensor", "wkt": "POINT(345.678 901.234)", "status": "inactive"}
# ]

# For each sensor, we would create a marker on the map:
# for sensor in sensors:
#     folium.Marker(location=[sensor['wkt'].y, sensor['wkt'].x], popup=sensor['name'] + ": " + sensor['status']).add_to(m)

# Save the final map
m.save("69.html")