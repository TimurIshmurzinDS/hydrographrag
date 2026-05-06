import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize the map centered on the basin centroid
m = folium.Map(location=basin.centroid.values[0], tiles='CartoDB positron', zoom_start=10)

# Add the basin to the map
folium.GeoJson(basin, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If coordinates are provided in the context, add them as markers
coordinates = [
    {'name': 'Терисбутак', 'coords': (43.1567, 77.8983)},
    {'name': 'Талгар', 'coords': (43.2000, 77.8000)}
]

for coord in coordinates:
    folium.Marker(location=coord['coords'], popup=coord['name']).add_to(m)

# Save the map
m.save("176.html")