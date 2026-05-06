import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Create map with basin boundaries
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(gdf.__geo_interface__, name='basin').add_to(m)
m

# Hardcoded list of dictionaries for river coordinates (WKT)
river_coords = [
    {'name': 'Shyzhyn River', 'wkt': 'POLYGON ((40.1234 45.6789, 40.2345 45.6789, 40.3456 46.7890, 40.4567 46.7890, 40.5678 45.6789))'},
    {'name': 'Sarykan River', 'wkt': 'POLYGON ((41.2345 47.8901, 41.3456 47.8901, 41.4567 48.9012, 41.5678 48.9012, 41.6789 47.8901))'}
]

# Add river coordinates to map
for coord in river_coords:
    folium.Marker([coord['wkt'].coords[0][1], coord['wkt'].coords[0][0]], popup=coord['name']).add_to(m)

# Save final map
m.save("165.html")