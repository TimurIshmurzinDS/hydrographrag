import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize the map centered on the basin centroid
m = folium.Map(location=basin.centroid.values[0], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Hardcoded list of dictionaries for hydroposts (replace with actual data)
hydroposts = [
    {'name': 'Hydropost 1', 'coordinates': wkt.loads('POINT (43.56789 35.67890)')},
    {'name': 'Hydropost 2', 'coordinates': wkt.loads('POINT (43.12345 35.98765)')}
]

# Add hydroposts to the map (replace with actual data and visualization logic)
for post in hydroposts:
    folium.Marker(location=[post['coordinates'].y, post['coordinates'].x], popup=post['name']).add_to(m)

# Save the map
m.save("76.html")