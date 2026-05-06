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
    basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# Create a hardcoded list of dictionaries with river coordinates in WKT format
rivers = [
    {'name': 'Шынжалы', 'wkt': 'LINESTRING(...)'},  # Replace (...) with actual coordinates
    {'name': 'Талгар', 'wkt': 'LINESTRING(...)'}   # Replace (...) with actual coordinates
]

# Add rivers to the map
for river in rivers:
    folium.GeoJson(
        wkt.loads(river['wkt']),
        style_function=lambda x: {'fillColor': 'red', 'color': 'darkred', 'fillOpacity': 0.8},
        tooltip=river['name']
    ).add_to(m)

# Save the final map
m.save("169.html")