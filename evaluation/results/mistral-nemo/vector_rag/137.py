import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If there are Coordinates (WKT) in the context, create a hardcoded list of dictionaries
coordinates = [
    {'name': 'Или река', 'wkt': 'POLYGON((...))'},  # Replace ... with actual coordinates
    {'name': 'Каратал река', 'wkt': 'POLYGON((...))'}  # Replace ... with actual coordinates
]

# Add rivers to the map using their WKT representations
for river in coordinates:
    folium.GeoJson(wkt.loads(river['wkt']), fillColor='blue', color='darkblue', fillOpacity=0.2).add_to(m)
    folium.Marker([river['wkt'].centroid.y, river['wkt'].centroid.x], popup=river['name']).add_to(m)

# Save the final map
m.save("137.html")