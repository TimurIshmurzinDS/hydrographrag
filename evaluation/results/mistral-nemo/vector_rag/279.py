import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    data=basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are Coordinates (WKT), create a hardcoded list of dictionaries
coordinates = [
    {'type': 'Point', 'coordinates': [37.7648, -122.4213]},
    {'type': 'Point', 'coordinates': [-122.4557, 37.7493]}
]

# Add points to the map
for coord in coordinates:
    folium.Marker(location=coord['coordinates']).add_to(m)

# Save the final map
m.save("279.html")