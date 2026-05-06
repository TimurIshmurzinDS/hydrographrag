import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
uzyn_kargaly_coords = [{'type': 'Point', 'coordinates': [45.123, 68.456]}]
byzhy_coords = [{'type': 'Point', 'coordinates': [46.789, 69.123]}]
shyzhyn_coords = [{'type': 'Point', 'coordinates': [47.345, 70.654]}]

# Add rivers to the map
folium.GeoJson(uzyn_kargaly_coords).add_to(m)
folium.GeoJson(byzhy_coords).add_to(m)
folium.GeoJson(shyzhyn_coords).add_to(m)

# Save the final map
m.save("219.html")