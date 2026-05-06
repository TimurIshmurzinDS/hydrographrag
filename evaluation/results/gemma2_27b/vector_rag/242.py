import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize map centered on basin centroid
m = folium.Map(location=basin.centroid.values[0], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Define points of interest (replace with actual coordinates from context)
points = [
    {'geometry': wkt.loads('POINT (1 1)')}, # Replace with actual coordinates
    {'geometry': wkt.loads('POINT (2 2)')}, # Replace with actual coordinates
    {'geometry': wkt.loads('POINT (3 3)')}, # Replace with actual coordinates
]

# Add points to the map
for point in points:
    folium.Marker(location=[point['geometry'].y, point['geometry'].x]).add_to(m)

# Save the map
m.save("242.html")