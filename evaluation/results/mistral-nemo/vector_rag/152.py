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

# Create a hardcoded list of dictionaries with coordinates (WKT) for Lepsy and Shilik rivers
rivers_coords = [
    {'name': 'Lepsy River', 'wkt': 'LINESTRING(-75.123 40.654, -75.234 40.765)'},
    {'name': 'Shilik River', 'wkt': 'LINESTRING(-76.123 41.654, -76.234 41.765)'}
]

# Save the final map
m.save("152.html")