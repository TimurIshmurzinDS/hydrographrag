import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(gdf.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    gdf,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
coordinates = [
    {'name': 'Улькен Алматы', 'wkt': 'POINT(71.4569 43.2583)'},
    {'name': 'Емель', 'wkt': 'POINT(70.9833 43.4167)'},
    {'name': 'Тентек', 'wkt': 'POINT(71.2333 43.5333)'}
]

# Add coordinates to the map
for coord in coordinates:
    folium.Marker(wkt.loads(coord['wkt']), popup=coord['name']).add_to(m)

# Save the final map
m.save("105.html")