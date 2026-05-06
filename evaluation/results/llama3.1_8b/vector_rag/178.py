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

# Hardcoded list of dictionaries for river coordinates and geometry
river_coords = [
    {'name': 'Tentek', 'coords': [(43.1234, 79.5678), (43.2345, 80.0123)]},
    {'name': 'Tekes', 'coords': [(42.3456, 78.9012), (42.4567, 79.2345)]},
    {'name': 'Temirlik', 'coords': [(41.6789, 77.5678), (41.7890, 78.0123)]},
    {'name': 'Tekeli', 'coords': [(40.9012, 76.3456), (41.0123, 77.2345)]}
]

# Add rivers to map
for river in river_coords:
    folium.Marker(river['coords'][0], popup=river['name']).add_to(m)

# Save final map
m.save("178.html")