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

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
sharyn_coords = [{'type': 'Point', 'coordinates': [43.1567, 69.867]}]
kishi_almaty_coords = [{'type': 'Point', 'coordinates': [43.2567, 70.123]}]

# Add points to the map
for coord in sharyn_coords:
    folium.Marker(wkt.loads(coord['type'] + '(' + ','.join(map(str, coord['coordinates'])) + ')'), popup='Sharyn River').add_to(m)
for coord in kishi_almaty_coords:
    folium.Marker(wkt.loads(coord['type'] + '(' + ','.join(map(str, coord['coordinates'])) + ')'), popup='Kishi Almaty River').add_to(m)

# Save the final map
m.save("131.html")