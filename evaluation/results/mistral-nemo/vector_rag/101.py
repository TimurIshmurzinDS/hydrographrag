import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(gdf.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    gdf,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# Coordinates of rivers in WKT format (hardcoded)
rivers_wkt = [
    {"name": "Тентек", "geom": wkt.loads("POINT(51.4378 39.6822)")},
    {"name": "Быж", "geom": wkt.loads("POINT(51.5432 39.7211)")},
    {"name": "Емель", "geom": wkt.loads("POINT(51.5087 39.6945)")}
]

# Add rivers to the map
for river in rivers_wkt:
    folium.Marker(location=river['geom'].coords, popup=river['name']).add_to(m)

# Save the final map
m.save("101.html")