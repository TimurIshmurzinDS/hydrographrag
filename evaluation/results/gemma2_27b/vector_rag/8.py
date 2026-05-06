import geopandas as gpd
import folium
from shapely import wkt

# Load the basin shapefile and convert to EPSG:4326
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium map centered on the basin centroid
m = folium.Map(location=basin.centroid.values[0], tiles='CartoDB positron', zoom_start=12)

# Add the basin to the map
folium.GeoJson(basin, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Hardcode observation points (replace with actual coordinates if available)
observations = [
    {'location': wkt.loads('POINT (78.1234 43.5678)')},  # Replace with actual coordinates
    {'location': wkt.loads('POINT (78.1234 43.5678)')},  # Replace with actual coordinates
    {'location': wkt.loads('POINT (78.1234 43.5678)')},  # Replace with actual coordinates
    {'location': wkt.loads('POINT (78.1234 43.5678)')},  # Replace with actual coordinates
]

# Add observation points to the map
for obs in observations:
    folium.Marker(location=[obs['location'].y, obs['location'].x]).add_to(m)

# Save the map
m.save("8.html")