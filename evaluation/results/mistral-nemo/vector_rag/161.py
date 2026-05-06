import geopandas as gpd
import folium
from shapely import wkt

# Load basin data and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize Folium map using the centroid of the shapefile
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')

# Add basin to the map with green fill and dark green border
folium.GeoJson(
    basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# Hardcoded list of dictionaries containing river coordinates in WKT format
rivers = [
    {"name": "Shynzhaly River", "wkt": "LINESTRING(..."},  # Replace ... with actual WKT coordinates
    {"name": "Shilik River", "wkt": "LINESTRING(..."},
    {"name": "Byzhy River", "wkt": "LINESTRING(..."}
]

# Add rivers to the map as red points
for river in rivers:
    folium.CircleMarker(
        location=tuple(wkt.loads(river['wkt']).centroid.coords[0]),
        color='red',
        radius=5,
    ).add_to(m)

# Save final map
m.save("161.html")