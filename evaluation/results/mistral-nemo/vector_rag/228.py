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

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
coordinates = [
    {"type": "Feature", "geometry": wkt.loads("POINT(74.56 -51.34)"), "properties": {"name": "Ayagoz River"}},
    {"type": "Feature", "geometry": wkt.loads("POINT(72.89 -50.12)"), "properties": {"name": "Byzhy River"}},
    {"type": "Feature", "geometry": wkt.loads("POINT(73.45 -49.67)"), "properties": {"name": "Shyzhyn River"}},
    {"type": "Feature", "geometry": wkt.loads("POINT(71.23 -50.89)"), "properties": {"name": "Bayankol River"}}
]

# Add the coordinates to the map
for coord in coordinates:
    folium.Marker(coord["geometry"], popup=coord["properties"]["name"]).add_to(m)

# Save the final map
m.save("228.html")