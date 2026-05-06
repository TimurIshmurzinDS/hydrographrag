import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Create map
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Add basin to map
folium.GeoJson(gdf.__geo_interface__, name='basin', color='darkgreen', fillOpacity=0.2).add_to(m)

# Create hardcoded list of dictionaries for coordinates (WKT)
wkt_coords = [
    {'type': 'Point', 'coordinates': [43.1234, 12.3456]},
    {'type': 'Point', 'coordinates': [43.2345, 12.4567]}
]

# Add points to map
for coord in wkt_coords:
    folium.Marker(coord['coordinates'], icon=folium.Icon(color='red')).add_to(m)

# Save final map
m.save("218.html")