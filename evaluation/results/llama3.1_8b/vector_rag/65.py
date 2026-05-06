import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Create map
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(gdf.__geo_interface__, name='basin', color='darkgreen', fillOpacity=0.2).add_to(m)

# Hardcoded list of dictionaries for coordinates (WKT)
coordinates = [
    {'lat': 45.1234, 'lon': 30.5678},
    {'lat': 40.9876, 'lon': 35.4321}
]

# Add markers to the map
for coord in coordinates:
    folium.Marker([coord['lat'], coord['lon']], popup='Marker').add_to(m)

# Save final map
m.save("65.html")