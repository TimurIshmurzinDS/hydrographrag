import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Create map
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Add basin to map
folium.GeoJson(basin_gdf.to_json(), name='basin').add_to(m)

# Hardcoded list of dictionaries for coordinates (WKT)
coordinates = [
    {'lat': 55.7558, 'lon': 37.6173},
    {'lat': 40.7128, 'lon': -74.0060}
]

# Add markers to map
for coord in coordinates:
    folium.Marker([coord['lat'], coord['lon']], popup='Корм').add_to(m)

# Save final map
m.save("276.html")