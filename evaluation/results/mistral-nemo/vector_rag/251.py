import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize Folium map with the centroid of the shapefile
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map using GeoJson
folium.GeoJson(
    basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are coordinates (WKT), create a hardcoded list of dictionaries and add them to the map as markers
coordinates = [
    {'lat': 51.5074, 'lon': -0.1278, 'popup': 'Point A'},
    {'lat': 51.5156, 'lon': -0.1398, 'popup': 'Point B'}
]
for coord in coordinates:
    folium.Marker(location=[coord['lat'], coord['lon']], popup=coord['popup']).add_to(m)

# Save the final map
m.save("251.html")