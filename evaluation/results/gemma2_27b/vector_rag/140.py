import geopandas as gpd
import folium
from shapely import wkt

# Load basin shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize map centered on the basin centroid
m = folium.Map(location=basin.centroid.values[0], tiles='CartoDB positron', zoom_start=8)

# Add basin to the map
folium.GeoJson(basin, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Hardcoded list of sensor coordinates (replace with actual data if available)
sensors = [
    {'name': 'Tokyraun Sensor 1', 'coordinates': wkt.loads('POINT(-76.9854 42.3089)')},
    {'name': 'Ayagoz Sensor 1', 'coordinates': wkt.loads('POINT(78.2497 43.8688)')}
]

# Add sensors to the map (replace with actual data if available)
for sensor in sensors:
    folium.Marker(location=[sensor['coordinates'].y, sensor['coordinates'].x], popup=sensor['name']).add_to(m)

# Save the map
m.save("140.html")