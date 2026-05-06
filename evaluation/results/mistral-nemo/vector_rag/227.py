import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
ili_river_coords = [
    {'type': 'Point', 'coordinates': [78.539641, 43.250987]},  # Example coordinate for Ili River
]

# Add river coordinates to the map
for coord in ili_river_coords:
    folium.Marker(wkt.loads(coord['type'] + '(' + ','.join(map(str, coord['coordinates'])) + ')')).add_to(m)

# Save the final map
m.save("227.html")