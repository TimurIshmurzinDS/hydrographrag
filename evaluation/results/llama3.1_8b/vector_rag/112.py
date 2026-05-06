import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Create map
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Add basin to map
folium.GeoJson(gdf.geometry.__geo_interface__, name='basin').add_to(m)

# Hardcoded list of dictionaries for river coordinates (WKT)
river_coords = [
    {'name': 'Kurty River', 'wkt': 'POINT(47.123 69.456)'},
    {'name': 'Urzhar River', 'wkt': 'POINT(48.789 68.321)'},
    {'name': 'Byzhy River', 'wkt': 'POINT(46.987 70.543)'}
]

# Add river coordinates to map
for coord in river_coords:
    folium.Marker(folium.Location([coord['wkt'].coords[1], coord['wkt'].coords[0]], popup=coord['name'])._repr_json_object_()).add_to(m)

# Save final map
m.save("112.html")