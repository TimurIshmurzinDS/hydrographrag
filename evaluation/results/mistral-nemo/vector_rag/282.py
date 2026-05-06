import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    data=r"data/basin_data.shp",
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are Coordinates (WKT), create a hardcoded list of dictionaries
coordinates = [
    {'type': 'Point', 'coordinates': [37.541, 55.737]},  # Example coordinate for Moscow
]

for coord in coordinates:
    folium.Marker(location=coord['coordinates']).add_to(m)

# Save the final map
m.save("282.html")