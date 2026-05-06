import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson
folium.GeoJson(
    basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
coordinates = [
    {"type": "Feature", "geometry": wkt.loads("POINT (-74.0060 4.5703)"), "properties": {"name": "Emel River"}},
    {"type": "Feature", "geometry": wkt.loads("POINT (-73.9812 4.6122)"), "properties": {"name": "Turgen River"}},
]

# Add the coordinates to the map using folium.Marker
for coord in coordinates:
    folium.Marker(location=coord["geometry"].coords[0]).add_to(m)

# Save the final map
m.save("207.html")