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
    data=basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# Hardcoded list of dictionaries with coordinates for each river in WKT format
rivers_coords = [
    {'name': 'Kurty River', 'wkt': 'POINT(74.56 -39.12)'},
    {'name': 'Tekes River', 'wkt': 'POINT(70.12 40.23)'}
]

# Add rivers to the map with their water consumption values
for river in rivers_coords:
    folium.Marker(
        location=tuple(wkt.loads(river['wkt']).xy),
        popup=f'River: {river["name"]}\nWater Consumption (m³/s): {water_consumption_values[river["name"]]}',
    ).add_to(m)

# Save the final map
m.save("129.html")