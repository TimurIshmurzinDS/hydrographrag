import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize Folium.Map using the centroid of the shapefile
m = folium.Map(location=[gdf.centroid.y, gdf.centroid.x], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(gdf, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If there are coordinates (WKT) for anomalies, create a hardcoded list of dictionaries
anomalies = [
    {'type': 'Feature', 'geometry': wkt.loads('POINT(74.56 41.23)'), 'properties': {'name': 'Karatal River Anomaly'}},
]

# Add anomalies to the map
for anomaly in anomalies:
    folium.Marker([anomaly['geometry'].y, anomaly['geometry'].x], popup=anomaly['properties']['name']).add_to(m)

# Save the final map
m.save("222.html")