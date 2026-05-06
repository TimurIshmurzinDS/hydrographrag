import geopandas as gpd
import folium
from shapely import wkt

# Load basin shapefile and convert to EPSG:4326
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize Folium map centered on the basin centroid
m = folium.Map(location=basin.centroid.values[0], tiles='CartoDB positron', zoom_start=10)

# Add basin boundary to the map
folium.GeoJson(basin, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Hardcoded list of sensor locations (replace with actual data if available)
sensors = [
    {'name': 'Sensor 1', 'coordinates': wkt.loads('POINT (-95.766 38.548)')},
    {'name': 'Sensor 2', 'coordinates': wkt.loads('POINT (-95.801 38.576)')},
]

# Add sensors to the map (replace with actual status and visualization logic)
for sensor in sensors:
    folium.Marker(location=[sensor['coordinates'].y, sensor['coordinates'].x], popup=sensor['name']).add_to(m)

# Save the map
m.save("136.html")