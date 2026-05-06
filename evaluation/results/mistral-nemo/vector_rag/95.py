import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    basin,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
coordinates = [
    {"type": "Feature", "geometry": wkt.loads("POINT(74.56 -3.14)")},
    {"type": "Feature", "geometry": wkt.loads("POINT(-0.12 55.86)")}
]

# Add the coordinates to the map
for coord in coordinates:
    folium.Marker(location=tuple(coord['geometry'].coords[0])).add_to(m)

# Save the final map
m.save("95.html")