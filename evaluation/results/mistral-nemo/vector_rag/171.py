import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson
folium.GeoJson(
    basin,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If coordinates are provided in WKT format, create a hardcoded list of dictionaries
coordinates = [
    {'type': 'Point', 'coordinates': (43.2516, 76.9498)},  # Example coordinate for Kiishi-Osek confluence with Osek River
    {'type': 'Point', 'coordinates': (43.2489, 76.9502)}  # Example coordinate for Talgar River confluence with Kiishi-Osek
]

# Add coordinates to the map using folium.Marker
for coord in coordinates:
    folium.Marker(location=coord['coordinates']).add_to(m)

# Save the final map
m.save("171.html")