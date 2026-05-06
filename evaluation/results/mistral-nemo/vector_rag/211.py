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

# If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
rivers = [
    {"name": "Uzyn Kargaly River", "wkt": "LINESTRING(...)"},  # Replace ... with actual WKT coordinates
    {"name": "Byzhy River", "wkt": "LINESTRING(...)"},
    {"name": "Shyzhyn River", "wkt": "LINESTRING(...)"},
    {"name": "Shynzhaly River", "wkt": "LINESTRING(...)"},
    {"name": "2 km above the mouth of Prokhodnoy River", "wkt": "POINT(...)"}  # Replace ... with actual WKT coordinates
]

# Add rivers to the map as GeoJson features
for river in rivers:
    folium.GeoJson(
        wkt.loads(river["wkt"]),
        style_function=lambda x: {'fillColor': 'blue', 'color': 'darkblue', 'fillOpacity': 0.2},
        highlight_function=lambda x: folium.GeoJson(
            wkt.loads(river["wkt"]),
            style_function=lambda y: {'fillColor': 'red', 'color': 'darkred', 'fillOpacity': 0.2},
        ).add_to(m),
    ).add_to(m)

# Save the final map
m.save("211.html")