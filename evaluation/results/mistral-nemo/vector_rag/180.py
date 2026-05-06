import geopandas as gpd
import folium
from shapely import wkt

# Load basin data and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map with the centroid of the shapefile
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')

# Add basin to the map
folium.GeoJson(
    data=basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are coordinates (WKT) for Tekes and Sarykan rivers, create a list of dictionaries
# with point data and add them to the map as markers

# Example: if coordinates exist
tekes_coords = [(74.56, 41.23), (74.60, 41.28)]
sarykan_coords = [(75.12, 41.56), (75.18, 41.62)]

points_data = [
    {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': coords}, 'properties': {}} for coords in tekes_coords + sarykan_coords
]

# Add points to the map as markers
for point in points_data:
    folium.Marker(location=point['geometry']['coordinates']).add_to(m)

# Save the final map
m.save("180.html")