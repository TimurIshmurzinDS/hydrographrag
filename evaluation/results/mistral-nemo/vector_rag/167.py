import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=gdf.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(gdf, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Hardcoded list of dictionaries for coordinates (WKT)
coordinates = [
    {'name': 'Tekes River', 'wkt': 'LINESTRING(-75.123 40.654, -74.987 40.789)'},
    {'name': 'Tentek River', 'wkt': 'LINESTRING(-76.234 41.321, -75.876 41.567)'}
]

# Calculate the total length of river network connecting Tekes and Tentek rivers
total_length = 0

for coord in coordinates:
    line = wkt.loads(coord['wkt'])
    length = line.length
    total_length += length

print(f'Общая протяженность речной сети, соединяющей реки Текес и Тентек: {total_length} км')

# Save the final map
m.save("167.html")