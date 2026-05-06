import geopandas as gpd
import folium
from shapely import wkt

# Load the basin shapefile and convert to EPSG:4326
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium map centered on the basin centroid
m = folium.Map(location=basin.centroid.values[0], tiles='CartoDB positron', zoom_start=10)

# Add the basin to the map
folium.GeoJson(basin, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Example: Hardcoded list of observation points (replace with actual data)
observations = [
    {'coordinates': wkt.loads('POINT (-117.1611 32.7157)'), 'name': 'Observation_1'},
]

# Add observation points to the map (replace with actual code to load and process observations)
for obs in observations:
    folium.Marker(location=obs['coordinates'], popup=obs['name']).add_to(m)

# Save the map
m.save("14.html")