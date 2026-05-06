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

# Create a hardcoded list of dictionaries with coordinates for Ural River, Dos River and Karatal River
rivers_coords = [
    {'name': 'Уржар река', 'coordinates': [(74.5683, 51.0925), (74.5683, 51.0925)]},
    {'name': 'Дос река', 'coordinates': [(74.5683, 51.0925), (74.5683, 51.0925)]},
    {'name': 'Каратал река', 'coordinates': [(74.5683, 51.0925), (74.5683, 51.0925)]}
]

# Add rivers coordinates to the map
for river in rivers_coords:
    folium.PolyLine(river['coordinates']).add_to(m)
    folium.Marker(river['coordinates'][0], popup=river['name']).add_to(m)

# Save the final map
m.save("103.html")