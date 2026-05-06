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

# Define Coordinates (WKT) for Kurty River, Urzhar River and Byzhy River
rivers_wkt = [
    {'name': 'Kurty River', 'wkt': 'POINT(74.56 51.34)'},
    {'name': 'Urzhar River', 'wkt': 'POINT(74.89 51.22)'},
    {'name': 'Byzhy River', 'wkt': 'POINT(74.23 51.45)'}
]

# Create a GeoDataFrame from the list of dictionaries
rivers_gdf = gpd.GeoDataFrame(rivers_wkt, geometry=[wkt.loads(wkt) for wkt in rivers_wkt['wkt']])

# Add rivers to the map
folium.GeoJson(rivers_gdf, fillColor='blue', color='blue', fillOpacity=0.5).add_to(m)

# Save the final map
m.save("112.html")